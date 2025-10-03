"""
API routes for data extraction services.

This module provides REST API endpoints for the automated data extraction system,
allowing clients to extract impact data for asteroids and specific locations.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.database import get_db
from api.services.data_extraction import DataExtractionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/data-extraction", tags=["data-extraction"])


@router.post("/extract")
async def extract_impact_data(
    asteroid_name: str,
    impact_latitude: float,
    impact_longitude: float,
    impact_altitude: float = None,
    db: Session = Depends(get_db)
):
    """
    Extract complete impact data for an asteroid and impact location.
    
    This endpoint performs automated extraction of:
    - Asteroid characteristics from NASA JPL
    - Topography/elevation from NASA CMR
    - Geological data from OneGeology
    - Regional data (faults, bathymetry, population, infrastructure)
    
    Args:
        asteroid_name: Name or designation of the asteroid
        impact_latitude: Impact latitude in decimal degrees
        impact_longitude: Impact longitude in decimal degrees
        impact_altitude: Impact altitude in meters (optional)
        db: Database session
        
    Returns:
        Dictionary with complete impact data or error information
    """
    try:
        logger.info(f"Starting data extraction for asteroid: {asteroid_name}")
        
        # Create data extraction service
        extraction_service = DataExtractionService(db)
        
        # Perform data extraction
        results = await extraction_service.extract_comprehensive_data(
            asteroid_name=asteroid_name,
            impact_latitude=impact_latitude,
            impact_longitude=impact_longitude,
            impact_altitude=impact_altitude
        )
        
        logger.info("Data extraction completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Data extraction endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Data extraction failed: {str(e)}"
        )


@router.post("/extract-async")
async def extract_impact_data_async(
    asteroid_name: str,
    impact_latitude: float,
    impact_longitude: float,
    impact_altitude: float = None,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start asynchronous data extraction and return extraction ID.
    
    This endpoint starts the extraction process in the background and returns
    immediately with an extraction ID that can be used to check status.
    
    Args:
        asteroid_name: Name or designation of the asteroid
        impact_latitude: Impact latitude in decimal degrees
        impact_longitude: Impact longitude in decimal degrees
        impact_altitude: Impact altitude in meters (optional)
        background_tasks: FastAPI background tasks for async processing
        db: Database session
        
    Returns:
        Dictionary with extraction ID and status URL
    """
    try:
        import uuid
        extraction_id = str(uuid.uuid4())
        
        # Start extraction in background
        background_tasks.add_task(
            async_extraction_worker,
            extraction_id,
            asteroid_name,
            impact_latitude,
            impact_longitude,
            impact_altitude,
            db
        )
        
        logger.info(f"Started async extraction with ID: {extraction_id}")
        
        return {
            "extraction_id": extraction_id,
            "status": "started",
            "status_url": f"/api/data-extraction/status/{extraction_id}",
            "estimated_completion_time": "5-10 minutes"
        }
        
    except Exception as e:
        logger.error(f"Async extraction start error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start extraction: {str(e)}"
        )


@router.get("/status/{extraction_id}")
async def get_extraction_status(extraction_id: str, db: Session = Depends(get_db)):
    """
    Get the status of an ongoing data extraction.
    
    Args:
        extraction_id: Unique identifier for the extraction
        db: Database session
        
    Returns:
        Dictionary with current progress and status
    """
    try:
        extraction_service = DataExtractionService(db)
        status = await extraction_service.get_extraction_status(extraction_id)
        return status
        
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=f"Extraction ID not found: {extraction_id}"
        )


@router.get("/asteroids/{asteroid_name}")
async def get_asteroid_data(asteroid_name: str):
    """
    Extract asteroid data from NASA JPL for a specific asteroid.
    
    Args:
        asteroid_name: Name or designation of the asteroid
        
    Returns:
        Dictionary with asteroid characteristics
    """
    try:
        from api.services.extractors.nasa_jpl_extractor import NASAJPLExtractor
        
        async with NASAJPLExtractor() as extractor:
            asteroid_data = await extractor.extract_asteroid_data(asteroid_name)
        
        if not asteroid_data:
            raise HTTPException(
                status_code=404,
                detail=f"Asteroid data not found for: {asteroid_name}"
            )
        
        return asteroid_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Asteroid data extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract asteroid data: {str(e)}"
        )


@router.get("/topography")
async def get_topography_data(
    latitude: float,
    longitude: float
):
    """
    Extract topography/elevation data for specific coordinates.
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        
    Returns:
        Dictionary with elevation information
    """
    try:
        from api.services.extractors.topography_extractor import TopographyExtractor
        
        async with TopographyExtractor() as extractor:
            topography_data = await extractor.extract_elevation_data(latitude, longitude)
        
        if not topography_data:
            raise HTTPException(
                status_code=404,
                detail=f"Topography data not found for coordinates: {latitude}, {longitude}"
            )
        
        return topography_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Topography data extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract topography data: {str(e)}"
        )


@router.get("/geology")
async def get_geological_data(
    latitude: float,
    longitude: float
):
    """
    Extract geological data for specific coordinates.
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        
    Returns:
        Dictionary with geological information
    """
    try:
        from api.services.extractors.geology_extractor import GeologyExtractor
        
        async with GeologyExtractor() as extractor:
            geological_data = await extractor.extract_geological_data(latitude, longitude)
        
        if not geological_data:
            raise HTTPException(
                status_code=404,
                detail=f"Geological data not found for coordinates: {latitude}, {longitude}"
            )
        
        return geological_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Geological data extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract geological data: {str(e)}"
        )


@router.get("/regional")
async def get_regional_data(
    latitude: float,
    longitude: float,
    radius_km: float = 100.0
):
    """
    Extract regional data for specific coordinates and radius.
    
    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        radius_km: Radius for regional data extraction in kilometers
        
    Returns:
        Dictionary with regional information
    """
    try:
        from api.services.extractors.regional_data_extractor import RegionalDataExtractor
        
        async with RegionalDataExtractor() as extractor:
            regional_data = await extractor.extract_regional_data(latitude, longitude, radius_km)
        
        if not regional_data:
            raise HTTPException(
                status_code=404,
                detail=f"Regional data not found for coordinates: {latitude}, {longitude}"
            )
        
        return regional_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Regional data extraction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract regional data: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for data extraction service.
    
    Returns:
        Dictionary with service status and available data sources
    """
    return {
        "status": "healthy",
        "service": "data-extraction",
        "available_data_sources": [
            "NASA JPL Small-Body Database",
            "NASA CMR Digital Elevation Model",
            "OneGeology Global Geological Map",
            "Global Active Faults Database",
            "GEBCO Bathymetry",
            "NASA SEDAC Population Data",
            "OpenStreetMap Infrastructure Data"
        ],
        "version": "1.0.0"
    }


# Background task functions
async def async_extraction_worker(
    extraction_id: str,
    asteroid_name: str,
    impact_latitude: float,
    impact_longitude: float,
    impact_altitude: float,
    db: Session
):
    """
    Background worker for asynchronous data extraction.
    
    Args:
        extraction_id: Unique identifier for the extraction
        asteroid_name: Name or designation of the asteroid
        impact_latitude: Impact latitude in decimal degrees
        impact_longitude: Impact longitude in decimal degrees
        impact_altitude: Impact altitude in meters
        db: Database session
    """
    try:
        logger.info(f"Starting background extraction: {extraction_id}")
        
        # Create data extraction service
        extraction_service = DataExtractionService(db)
        
        # Perform extraction
        results = await extraction_service.extract_comprehensive_data(
            asteroid_name=asteroid_name,
            impact_latitude=impact_latitude,
            impact_longitude=impact_longitude,
            impact_altitude=impact_altitude,
            extraction_id=extraction_id
        )
        
        logger.info(f"Background extraction completed: {extraction_id}")
        return results
            
    except Exception as e:
        logger.error(f"Background extraction worker error: {str(e)}")
        raise

