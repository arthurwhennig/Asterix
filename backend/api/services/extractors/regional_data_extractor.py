"""
Regional Data Extractor

This module extracts regional data including fault lines, bathymetry, population,
and infrastructure data for impact simulation analysis.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import httpx
import json
import math
import os
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.wkt import loads
import rasterio
from rasterio.warp import transform
from rasterio.crs import CRS

logger = logging.getLogger(__name__)


class RegionalDataExtractor:
    """Extractor for regional data including faults, bathymetry, population, and infrastructure."""
    
    # Data sources and URLs
    DATA_SOURCES = {
        "faults": {
            "url": "https://github.com/GEMScienceTools/gem-global-active-faults/raw/main/gem-global-active-faults.shp",
            "local_path": "data/faults/global_active_faults.shp",
            "description": "Global Active Faults database from GEM Foundation"
        },
        "bathymetry": {
            "url": "https://www.gebco.net/data_and_products/gridded_bathymetry_data/",
            "local_path": "data/bathymetry/gebco_2023.nc",
            "description": "GEBCO global bathymetry grid"
        },
        "population": {
            "url": "https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density-rev11",
            "local_path": "data/population/gpw_v4_population_density_rev11_2020_30_sec.tif",
            "description": "NASA SEDAC population density grid"
        },
        "infrastructure": {
            "url": "https://download.geofabrik.de/",
            "local_path": "data/infrastructure/",
            "description": "OpenStreetMap infrastructure data"
        }
    }
    
    def __init__(self, data_dir: str = "data", timeout: int = 60):
        self.data_dir = Path(data_dir)
        self.timeout = timeout
        self.session = None
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory structure exists."""
        for source_config in self.DATA_SOURCES.values():
            local_path = Path(source_config["local_path"])
            if not local_path.is_absolute():
                local_path = self.data_dir / local_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def extract_regional_data(
        self, 
        latitude: float, 
        longitude: float,
        radius_km: float = 100.0
    ) -> Dict[str, Any]:
        """
        Extract regional data for given coordinates and radius.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            radius_km: Search radius in kilometers
            
        Returns:
            Dictionary containing regional data
            
        Raises:
            Exception: If data extraction fails
        """
        try:
            # Validate coordinates
            if not (-90 <= latitude <= 90):
                raise ValueError(f"Invalid latitude: {latitude}")
            if not (-180 <= longitude <= 180):
                raise ValueError(f"Invalid longitude: {longitude}")
            
            # Create search area
            search_area = self._create_search_area(latitude, longitude, radius_km)
            
            # Extract different types of regional data
            fault_data = await self._extract_fault_data(latitude, longitude, search_area)
            bathymetry_data = await self._extract_bathymetry_data(latitude, longitude)
            population_data = await self._extract_population_data(latitude, longitude, radius_km)
            infrastructure_data = await self._extract_infrastructure_data(latitude, longitude, radius_km)
            
            # Combine all data
            regional_data = {
                "latitude": latitude,
                "longitude": longitude,
                "search_radius_km": radius_km,
                "fault_data": fault_data,
                "bathymetry_data": bathymetry_data,
                "population_data": population_data,
                "infrastructure_data": infrastructure_data,
                "extracted_at": datetime.utcnow().isoformat(),
                "data_sources": self.DATA_SOURCES
            }
            
            logger.info(f"Successfully extracted regional data for ({latitude}, {longitude})")
            return regional_data
            
        except Exception as e:
            logger.error(f"Error extracting regional data for ({latitude}, {longitude}): {e}")
            raise
    
    def _create_search_area(self, latitude: float, longitude: float, radius_km: float) -> Polygon:
        """Create a search area polygon around the given coordinates."""
        # Convert radius from km to degrees (approximate)
        radius_deg = radius_km / 111.0  # 1 degree ≈ 111 km
        
        # Create a square search area
        min_lon = longitude - radius_deg
        max_lon = longitude + radius_deg
        min_lat = latitude - radius_deg
        max_lat = latitude + radius_deg
        
        return Polygon([
            (min_lon, min_lat),
            (max_lon, min_lat),
            (max_lon, max_lat),
            (min_lon, max_lat),
            (min_lon, min_lat)
        ])
    
    async def _extract_fault_data(
        self, 
        latitude: float, 
        longitude: float, 
        search_area: Polygon
    ) -> Dict[str, Any]:
        """Extract fault line data."""
        try:
            # Check if fault data exists locally
            fault_path = self.data_dir / "faults" / "global_active_faults.shp"
            
            if not fault_path.exists():
                logger.warning("Fault data not available locally. Using default values.")
                return self._get_default_fault_data()
            
            # Load fault data
            try:
                faults_gdf = gpd.read_file(fault_path)
                
                # Create point for distance calculation
                impact_point = Point(longitude, latitude)
                
                # Find faults within search area
                faults_in_area = faults_gdf[faults_gdf.geometry.intersects(search_area)]
                
                if faults_in_area.empty:
                    return self._get_default_fault_data()
                
                # Calculate distances to all faults
                distances = []
                for idx, fault in faults_in_area.iterrows():
                    distance = impact_point.distance(fault.geometry)
                    distances.append({
                        "distance_km": distance * 111.0,  # Convert to km
                        "fault_name": fault.get("Fault_Name", "Unknown"),
                        "fault_type": fault.get("Fault_Type", "Unknown"),
                        "slip_rate": fault.get("Slip_Rate", 0.0),
                        "activity": fault.get("Activity", "Unknown")
                    })
                
                # Find nearest fault
                nearest_fault = min(distances, key=lambda x: x["distance_km"])
                
                return {
                    "nearest_fault": nearest_fault,
                    "total_faults_in_area": len(distances),
                    "faults": distances[:10]  # Limit to 10 closest faults
                }
                
            except Exception as e:
                logger.error(f"Error reading fault data: {e}")
                return self._get_default_fault_data()
                
        except Exception as e:
            logger.error(f"Error extracting fault data: {e}")
            return self._get_default_fault_data()
    
    async def _extract_bathymetry_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Extract bathymetry data."""
        try:
            # Check if bathymetry data exists locally
            bathymetry_path = self.data_dir / "bathymetry" / "gebco_2023.nc"
            
            if not bathymetry_path.exists():
                logger.warning("Bathymetry data not available locally. Using default values.")
                return self._get_default_bathymetry_data()
            
            # Read bathymetry value
            try:
                with rasterio.open(bathymetry_path) as dataset:
                    # Sample the raster at the point
                    values = list(dataset.sample([(longitude, latitude)]))
                    
                    if values:
                        depth = float(values[0][0])
                        is_land = depth > 0
                        
                        return {
                            "depth_m": abs(depth) if not is_land else 0.0,
                            "is_land": is_land,
                            "elevation_m": depth if is_land else 0.0
                        }
                    else:
                        return self._get_default_bathymetry_data()
                        
            except Exception as e:
                logger.error(f"Error reading bathymetry data: {e}")
                return self._get_default_bathymetry_data()
                
        except Exception as e:
            logger.error(f"Error extracting bathymetry data: {e}")
            return self._get_default_bathymetry_data()
    
    async def _extract_population_data(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float
    ) -> Dict[str, Any]:
        """Extract population data."""
        try:
            # Check if population data exists locally
            population_path = self.data_dir / "population" / "gpw_v4_population_density_rev11_2020_30_sec.tif"
            
            if not population_path.exists():
                logger.warning("Population data not available locally. Using default values.")
                return self._get_default_population_data()
            
            # Read population data
            try:
                with rasterio.open(population_path) as dataset:
                    # Create search area
                    search_area = self._create_search_area(latitude, longitude, radius_km)
                    
                    # Sample population density at impact point
                    values = list(dataset.sample([(longitude, latitude)]))
                    impact_population_density = float(values[0][0]) if values else 0.0
                    
                    # Calculate total population in affected area
                    # This is a simplified calculation
                    area_km2 = math.pi * (radius_km ** 2)
                    total_population = int(impact_population_density * area_km2)
                    
                    return {
                        "population_density_km2": impact_population_density,
                        "total_population": total_population,
                        "affected_area_km2": area_km2,
                        "major_cities": []  # Would need additional data for this
                    }
                    
            except Exception as e:
                logger.error(f"Error reading population data: {e}")
                return self._get_default_population_data()
                
        except Exception as e:
            logger.error(f"Error extracting population data: {e}")
            return self._get_default_population_data()
    
    async def _extract_infrastructure_data(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float
    ) -> Dict[str, Any]:
        """Extract infrastructure data."""
        try:
            # This would typically involve querying OpenStreetMap data
            # For now, return default infrastructure data
            return {
                "airports": [],
                "ports": [],
                "power_plants": [],
                "hospitals": [],
                "schools": [],
                "roads": [],
                "railways": []
            }
            
        except Exception as e:
            logger.error(f"Error extracting infrastructure data: {e}")
            return self._get_default_infrastructure_data()
    
    def _get_default_fault_data(self) -> Dict[str, Any]:
        """Get default fault data when no specific data is available."""
        return {
            "nearest_fault": {
                "distance_km": 50.0,
                "fault_name": "Unknown",
                "fault_type": "Unknown",
                "slip_rate": 0.0,
                "activity": "Unknown"
            },
            "total_faults_in_area": 0,
            "faults": []
        }
    
    def _get_default_bathymetry_data(self) -> Dict[str, Any]:
        """Get default bathymetry data when no specific data is available."""
        return {
            "depth_m": 0.0,
            "is_land": True,
            "elevation_m": 0.0
        }
    
    def _get_default_population_data(self) -> Dict[str, Any]:
        """Get default population data when no specific data is available."""
        return {
            "population_density_km2": 0.0,
            "total_population": 0,
            "affected_area_km2": 0.0,
            "major_cities": []
        }
    
    def _get_default_infrastructure_data(self) -> Dict[str, Any]:
        """Get default infrastructure data when no specific data is available."""
        return {
            "airports": [],
            "ports": [],
            "power_plants": [],
            "hospitals": [],
            "schools": [],
            "roads": [],
            "railways": []
        }
    
    async def download_data_sources(self, force_download: bool = False) -> Dict[str, bool]:
        """Download required data sources."""
        results = {}
        
        for source_name, config in self.DATA_SOURCES.items():
            try:
                local_path = Path(config["local_path"])
                if not local_path.is_absolute():
                    local_path = self.data_dir / local_path
                
                if local_path.exists() and not force_download:
                    results[source_name] = True
                    logger.info(f"Data source {source_name} already exists")
                    continue
                
                # Download data (simplified - would need actual download logic)
                logger.info(f"Downloading {source_name} data...")
                # This would involve actual download logic
                results[source_name] = False
                
            except Exception as e:
                logger.error(f"Error downloading {source_name}: {e}")
                results[source_name] = False
        
        return results


# Example usage and testing
async def test_extractor():
    """Test function for the regional data extractor."""
    async with RegionalDataExtractor() as extractor:
        try:
            # Test with coordinates in Colorado, USA
            data = await extractor.extract_regional_data(39.7392, -104.9903, 50.0)
            print("Extracted regional data:")
            print(f"Fault data: {data['fault_data']}")
            print(f"Bathymetry data: {data['bathymetry_data']}")
            print(f"Population data: {data['population_data']}")
            print(f"Infrastructure data: {data['infrastructure_data']}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_extractor())