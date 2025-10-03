"""
Main Data Extraction Service

This module orchestrates all data extractors to provide comprehensive
data extraction for asteroid impact simulation.
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from .extractors.nasa_jpl_extractor import NASAJPLExtractor
from .extractors.topography_extractor import TopographyExtractor
from .extractors.geology_extractor import GeologyExtractor
from .extractors.regional_data_extractor import RegionalDataExtractor
from .impact_calculator import ImpactCalculator
from database.models import (
    ExtractionSession, ExtractedAsteroidData, ExtractedTopographyData,
    ExtractedGeologicalData, ExtractedRegionalData, ImpactCalculation
)

logger = logging.getLogger(__name__)


class DataExtractionService:
    """Main service for orchestrating data extraction and impact calculations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.impact_calculator = ImpactCalculator()
    
    async def extract_comprehensive_data(
        self,
        asteroid_name: str,
        impact_latitude: float,
        impact_longitude: float,
        impact_altitude: float = None,
        extraction_id: str = None
    ) -> Dict[str, Any]:
        """
        Extract comprehensive data for asteroid impact simulation.
        
        Args:
            asteroid_name: Name or designation of the asteroid
            impact_latitude: Impact latitude in decimal degrees
            impact_longitude: Impact longitude in decimal degrees
            impact_altitude: Impact altitude in meters (optional)
            extraction_id: Unique extraction session ID (optional)
            
        Returns:
            Dictionary containing all extracted data and calculations
        """
        if not extraction_id:
            extraction_id = str(uuid.uuid4())
        
        # Create extraction session
        session = self._create_extraction_session(
            extraction_id, asteroid_name, impact_latitude, 
            impact_longitude, impact_altitude
        )
        
        try:
            # Update session status
            session.status = "in_progress"
            session.current_step = "Extracting asteroid data"
            self.db.commit()
            
            # Extract asteroid data
            asteroid_data = await self._extract_asteroid_data(asteroid_name, session)
            
            # Update progress
            session.progress_percentage = 20.0
            session.current_step = "Extracting topography data"
            self.db.commit()
            
            # Extract topography data
            topography_data = await self._extract_topography_data(
                impact_latitude, impact_longitude, session
            )
            
            # Update progress
            session.progress_percentage = 40.0
            session.current_step = "Extracting geological data"
            self.db.commit()
            
            # Extract geological data
            geological_data = await self._extract_geological_data(
                impact_latitude, impact_longitude, session
            )
            
            # Update progress
            session.progress_percentage = 60.0
            session.current_step = "Extracting regional data"
            self.db.commit()
            
            # Extract regional data
            regional_data = await self._extract_regional_data(
                impact_latitude, impact_longitude, session
            )
            
            # Update progress
            session.progress_percentage = 80.0
            session.current_step = "Calculating impact effects"
            self.db.commit()
            
            # Calculate impact effects
            impact_calculation = await self._calculate_impact_effects(
                asteroid_data, topography_data, geological_data, 
                regional_data, session
            )
            
            # Update progress
            session.progress_percentage = 100.0
            session.status = "completed"
            session.current_step = "Completed"
            session.extraction_time_seconds = (
                datetime.utcnow() - session.created_at
            ).total_seconds()
            self.db.commit()
            
            # Return comprehensive results
            return {
                "extraction_session": {
                    "id": extraction_id,
                    "status": "completed",
                    "progress_percentage": 100.0,
                    "extraction_time_seconds": session.extraction_time_seconds
                },
                "asteroid_data": asteroid_data,
                "topography_data": topography_data,
                "geological_data": geological_data,
                "regional_data": regional_data,
                "impact_calculation": impact_calculation,
                "extracted_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            # Update session with error
            session.status = "failed"
            session.current_step = f"Error: {str(e)}"
            session.errors = [{"error": str(e), "timestamp": datetime.utcnow().isoformat()}]
            self.db.commit()
            
            logger.error(f"Data extraction failed for session {extraction_id}: {e}")
            raise
    
    def _create_extraction_session(
        self,
        extraction_id: str,
        asteroid_name: str,
        impact_latitude: float,
        impact_longitude: float,
        impact_altitude: float = None
    ) -> ExtractionSession:
        """Create a new extraction session."""
        session = ExtractionSession(
            extraction_id=extraction_id,
            asteroid_name=asteroid_name,
            impact_latitude=impact_latitude,
            impact_longitude=impact_longitude,
            impact_altitude=impact_altitude,
            status="pending",
            progress_percentage=0.0,
            current_step="Initializing",
            data_sources={
                "nasa_jpl": "NASA JPL Small-Body Database",
                "nasa_cmr": "NASA Common Metadata Repository",
                "onegeology": "OneGeology WFS",
                "regional": "Regional geological and infrastructure data"
            }
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    async def _extract_asteroid_data(
        self, 
        asteroid_name: str, 
        session: ExtractionSession
    ) -> Dict[str, Any]:
        """Extract asteroid data using NASA JPL extractor."""
        try:
            async with NASAJPLExtractor() as extractor:
                asteroid_data = await extractor.extract_asteroid_data(asteroid_name)
                
                # Save to database
                db_asteroid_data = ExtractedAsteroidData(
                    extraction_session_id=session.id,
                    name=asteroid_data["name"],
                    nasa_id=asteroid_data["nasa_id"],
                    diameter_m=asteroid_data["diameter_m"],
                    velocity_ms=asteroid_data["velocity_ms"],
                    mass_kg=asteroid_data.get("mass_kg"),
                    composition=asteroid_data["composition"],
                    orbital_data=asteroid_data["orbital_data"],
                    close_approach_data=asteroid_data["close_approach_data"],
                    is_potentially_hazardous=asteroid_data["is_potentially_hazardous"]
                )
                
                self.db.add(db_asteroid_data)
                self.db.commit()
                
                return asteroid_data
                
        except Exception as e:
            logger.error(f"Error extracting asteroid data: {e}")
            raise
    
    async def _extract_topography_data(
        self,
        latitude: float,
        longitude: float,
        session: ExtractionSession
    ) -> Dict[str, Any]:
        """Extract topography data using NASA CMR extractor."""
        try:
            async with TopographyExtractor() as extractor:
                topography_data = await extractor.extract_elevation_data(latitude, longitude)
                
                # Save to database
                db_topography_data = ExtractedTopographyData(
                    extraction_session_id=session.id,
                    latitude=latitude,
                    longitude=longitude,
                    altitude=topography_data.get("altitude"),
                    elevation_m=topography_data["elevation_m"],
                    data_source=topography_data["data_source"],
                    resolution_m=topography_data.get("resolution_m"),
                    confidence_level=topography_data.get("confidence_level")
                )
                
                self.db.add(db_topography_data)
                self.db.commit()
                
                return topography_data
                
        except Exception as e:
            logger.error(f"Error extracting topography data: {e}")
            raise
    
    async def _extract_geological_data(
        self,
        latitude: float,
        longitude: float,
        session: ExtractionSession
    ) -> Dict[str, Any]:
        """Extract geological data using OneGeology extractor."""
        try:
            async with GeologyExtractor() as extractor:
                geological_data = await extractor.extract_geological_data(latitude, longitude)
                
                # Save to database
                db_geological_data = ExtractedGeologicalData(
                    extraction_session_id=session.id,
                    latitude=latitude,
                    longitude=longitude,
                    altitude=geological_data.get("altitude"),
                    geological_description=geological_data["geological_description"],
                    material_type=geological_data["material_type"],
                    density_kg_m3=geological_data["density_kg_m3"],
                    age_period=geological_data.get("age_period"),
                    formation_name=geological_data.get("formation_name"),
                    data_source=geological_data["data_source"]
                )
                
                self.db.add(db_geological_data)
                self.db.commit()
                
                return geological_data
                
        except Exception as e:
            logger.error(f"Error extracting geological data: {e}")
            raise
    
    async def _extract_regional_data(
        self,
        latitude: float,
        longitude: float,
        session: ExtractionSession
    ) -> Dict[str, Any]:
        """Extract regional data using regional data extractor."""
        try:
            async with RegionalDataExtractor() as extractor:
                regional_data = await extractor.extract_regional_data(latitude, longitude)
                
                # Save to database
                db_regional_data = ExtractedRegionalData(
                    extraction_session_id=session.id,
                    latitude=latitude,
                    longitude=longitude,
                    altitude=regional_data.get("altitude"),
                    
                    # Fault data
                    fault_name=regional_data["fault_data"]["nearest_fault"]["fault_name"],
                    fault_distance_km=regional_data["fault_data"]["nearest_fault"]["distance_km"],
                    fault_type=regional_data["fault_data"]["nearest_fault"]["fault_type"],
                    fault_activity_status=regional_data["fault_data"]["nearest_fault"]["activity"],
                    fault_slip_rate=regional_data["fault_data"]["nearest_fault"]["slip_rate"],
                    
                    # Bathymetry data
                    depth_m=regional_data["bathymetry_data"]["depth_m"],
                    is_land=regional_data["bathymetry_data"]["is_land"],
                    
                    # Population data
                    total_population=regional_data["population_data"]["total_population"],
                    population_density_km2=regional_data["population_data"]["population_density_km2"],
                    affected_area_km2=regional_data["population_data"]["affected_area_km2"],
                    major_cities=regional_data["population_data"]["major_cities"],
                    
                    # Infrastructure data
                    airports=regional_data["infrastructure_data"]["airports"],
                    ports=regional_data["infrastructure_data"]["ports"],
                    power_plants=regional_data["infrastructure_data"]["power_plants"],
                    hospitals=regional_data["infrastructure_data"]["hospitals"],
                    schools=regional_data["infrastructure_data"]["schools"]
                )
                
                self.db.add(db_regional_data)
                self.db.commit()
                
                return regional_data
                
        except Exception as e:
            logger.error(f"Error extracting regional data: {e}")
            raise
    
    async def _calculate_impact_effects(
        self,
        asteroid_data: Dict[str, Any],
        topography_data: Dict[str, Any],
        geological_data: Dict[str, Any],
        regional_data: Dict[str, Any],
        session: ExtractionSession
    ) -> Dict[str, Any]:
        """Calculate impact effects using all extracted data."""
        try:
            # Extract parameters for impact calculation
            asteroid_diameter_m = asteroid_data["diameter_m"]
            asteroid_velocity_ms = asteroid_data["velocity_ms"]
            asteroid_density_kg_m3 = 3000.0  # Default asteroid density
            
            target_density_kg_m3 = geological_data["density_kg_m3"]
            elevation_m = topography_data["elevation_m"]
            is_land = regional_data["bathymetry_data"]["is_land"]
            water_depth_m = regional_data["bathymetry_data"]["depth_m"]
            
            # Calculate impact effects
            impact_effects = self.impact_calculator.calculate_impact_effects(
                asteroid_diameter_m=asteroid_diameter_m,
                asteroid_velocity_ms=asteroid_velocity_ms,
                asteroid_density_kg_m3=asteroid_density_kg_m3,
                target_density_kg_m3=target_density_kg_m3,
                impact_latitude=session.impact_latitude,
                impact_longitude=session.impact_longitude,
                elevation_m=elevation_m,
                is_land=is_land,
                water_depth_m=water_depth_m
            )
            
            # Save to database
            db_impact_calculation = ImpactCalculation(
                extraction_session_id=session.id,
                impact_energy_joules=impact_effects["impact_energy"]["joules"],
                impact_energy_megatons=impact_effects["impact_energy"]["megatons_tnt"],
                crater_diameter_km=impact_effects["crater"]["diameter_km"],
                crater_depth_km=impact_effects["crater"]["depth_km"],
                fireball_radius_km=impact_effects["airblast"]["fireball_radius_km"],
                thermal_radiation_radius_km=impact_effects["thermal"]["thermal_radius_km"],
                blast_wave_radius_km=max(impact_effects["airblast"]["blast_radii_km"].values()),
                richter_magnitude=impact_effects["earthquake"]["richter_magnitude"],
                tsunami_wave_height_meters=impact_effects["tsunami"]["initial_wave_height_m"] if impact_effects["tsunami"] else None,
                calculation_method="simplified_scaling_laws",
                calculation_version="1.0",
                calculation_metadata=impact_effects
            )
            
            self.db.add(db_impact_calculation)
            self.db.commit()
            
            return impact_effects
            
        except Exception as e:
            logger.error(f"Error calculating impact effects: {e}")
            raise
    
    async def get_extraction_status(self, extraction_id: str) -> Dict[str, Any]:
        """Get the status of an extraction session."""
        session = self.db.query(ExtractionSession).filter(
            ExtractionSession.extraction_id == extraction_id
        ).first()
        
        if not session:
            raise ValueError(f"Extraction session {extraction_id} not found")
        
        return {
            "extraction_id": extraction_id,
            "status": session.status,
            "progress_percentage": session.progress_percentage,
            "current_step": session.current_step,
            "errors": session.errors,
            "warnings": session.warnings,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }
    
    async def get_extraction_results(self, extraction_id: str) -> Dict[str, Any]:
        """Get the results of a completed extraction session."""
        session = self.db.query(ExtractionSession).filter(
            ExtractionSession.extraction_id == extraction_id
        ).first()
        
        if not session:
            raise ValueError(f"Extraction session {extraction_id} not found")
        
        if session.status != "completed":
            raise ValueError(f"Extraction session {extraction_id} is not completed")
        
        # Get all related data
        asteroid_data = self.db.query(ExtractedAsteroidData).filter(
            ExtractedAsteroidData.extraction_session_id == session.id
        ).first()
        
        topography_data = self.db.query(ExtractedTopographyData).filter(
            ExtractedTopographyData.extraction_session_id == session.id
        ).first()
        
        geological_data = self.db.query(ExtractedGeologicalData).filter(
            ExtractedGeologicalData.extraction_session_id == session.id
        ).first()
        
        regional_data = self.db.query(ExtractedRegionalData).filter(
            ExtractedRegionalData.extraction_session_id == session.id
        ).first()
        
        impact_calculation = self.db.query(ImpactCalculation).filter(
            ImpactCalculation.extraction_session_id == session.id
        ).first()
        
        return {
            "extraction_session": {
                "id": extraction_id,
                "asteroid_name": session.asteroid_name,
                "impact_latitude": session.impact_latitude,
                "impact_longitude": session.impact_longitude,
                "impact_altitude": session.impact_altitude,
                "status": session.status,
                "extraction_time_seconds": session.extraction_time_seconds
            },
            "asteroid_data": {
                "name": asteroid_data.name,
                "nasa_id": asteroid_data.nasa_id,
                "diameter_m": asteroid_data.diameter_m,
                "velocity_ms": asteroid_data.velocity_ms,
                "mass_kg": asteroid_data.mass_kg,
                "composition": asteroid_data.composition,
                "is_potentially_hazardous": asteroid_data.is_potentially_hazardous
            } if asteroid_data else None,
            "topography_data": {
                "elevation_m": topography_data.elevation_m,
                "resolution_m": topography_data.resolution_m,
                "confidence_level": topography_data.confidence_level
            } if topography_data else None,
            "geological_data": {
                "geological_description": geological_data.geological_description,
                "material_type": geological_data.material_type,
                "density_kg_m3": geological_data.density_kg_m3,
                "age_period": geological_data.age_period,
                "formation_name": geological_data.formation_name
            } if geological_data else None,
            "regional_data": {
                "fault_data": {
                    "nearest_fault": {
                        "name": regional_data.fault_name,
                        "distance_km": regional_data.fault_distance_km,
                        "type": regional_data.fault_type,
                        "activity": regional_data.fault_activity_status
                    }
                },
                "bathymetry_data": {
                    "depth_m": regional_data.depth_m,
                    "is_land": regional_data.is_land
                },
                "population_data": {
                    "total_population": regional_data.total_population,
                    "population_density_km2": regional_data.population_density_km2,
                    "affected_area_km2": regional_data.affected_area_km2
                }
            } if regional_data else None,
            "impact_calculation": {
                "impact_energy_joules": impact_calculation.impact_energy_joules,
                "impact_energy_megatons": impact_calculation.impact_energy_megatons,
                "crater_diameter_km": impact_calculation.crater_diameter_km,
                "crater_depth_km": impact_calculation.crater_depth_km,
                "fireball_radius_km": impact_calculation.fireball_radius_km,
                "thermal_radiation_radius_km": impact_calculation.thermal_radiation_radius_km,
                "blast_wave_radius_km": impact_calculation.blast_wave_radius_km,
                "richter_magnitude": impact_calculation.richter_magnitude,
                "tsunami_wave_height_meters": impact_calculation.tsunami_wave_height_meters,
                "calculation_metadata": impact_calculation.calculation_metadata
            } if impact_calculation else None
        }