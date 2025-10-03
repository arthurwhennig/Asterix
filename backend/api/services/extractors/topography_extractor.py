"""
NASA CMR Topography Extractor

This module extracts elevation data from NASA's Common Metadata Repository (CMR)
using STAC (SpatioTemporal Asset Catalog) to get ground elevation at impact coordinates.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import httpx
import rasterio
from rasterio.warp import transform
from rasterio.crs import CRS
import numpy as np
from shapely.geometry import Point
import json

logger = logging.getLogger(__name__)


class TopographyExtractor:
    """Extractor for elevation data from NASA CMR using STAC."""
    
    CMR_STAC_ENDPOINT = "https://cmr.earthdata.nasa.gov/stac/LPCLOUD"
    
    # Available elevation datasets
    ELEVATION_COLLECTIONS = [
        "COP-DEM_GLO-30-DGED",  # Copernicus Digital Elevation Model
        "HLSL30",               # Harmonized Landsat Sentinel-2
        "ASTER_GDEM_V003",      # ASTER Global Digital Elevation Model
        "SRTMGL1_v003"          # Shuttle Radar Topography Mission
    ]
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def extract_elevation_data(
        self, 
        latitude: float, 
        longitude: float,
        collection: str = "COP-DEM_GLO-30-DGED"
    ) -> Dict[str, Any]:
        """
        Extract elevation data for given coordinates.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            collection: STAC collection name for elevation data
            
        Returns:
            Dictionary containing elevation data
            
        Raises:
            Exception: If data extraction fails
        """
        try:
            # Validate coordinates
            if not (-90 <= latitude <= 90):
                raise ValueError(f"Invalid latitude: {latitude}")
            if not (-180 <= longitude <= 180):
                raise ValueError(f"Invalid longitude: {longitude}")
            
            # Search for available data
            search_results = await self._search_elevation_data(latitude, longitude, collection)
            
            if not search_results.get("features"):
                raise Exception(f"No elevation data found for coordinates ({latitude}, {longitude})")
            
            # Get the best matching feature
            best_feature = self._select_best_feature(search_results["features"])
            
            # Extract elevation value
            elevation_data = await self._extract_elevation_value(
                best_feature, latitude, longitude
            )
            
            # Add metadata
            elevation_data.update({
                "latitude": latitude,
                "longitude": longitude,
                "data_source": "NASA CMR",
                "collection": collection,
                "extracted_at": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Successfully extracted elevation data for ({latitude}, {longitude})")
            return elevation_data
            
        except Exception as e:
            logger.error(f"Error extracting elevation data for ({latitude}, {longitude}): {e}")
            raise
    
    async def _search_elevation_data(
        self, 
        latitude: float, 
        longitude: float, 
        collection: str
    ) -> Dict[str, Any]:
        """Search for elevation data using STAC API."""
        try:
            # Create a small bounding box around the point
            bbox_size = 0.01  # degrees
            bbox = [
                longitude - bbox_size,
                latitude - bbox_size,
                longitude + bbox_size,
                latitude + bbox_size
            ]
            
            # Construct STAC search request
            search_params = {
                "collections": [collection],
                "bbox": bbox,
                "limit": 10,
                "datetime": "2020-01-01T00:00:00Z/.."  # Recent data
            }
            
            # Make STAC search request
            response = await self.session.post(
                f"{self.CMR_STAC_ENDPOINT}/search",
                json=search_params,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during STAC search: {e}")
            raise Exception(f"Failed to search elevation data: {e}")
        except Exception as e:
            logger.error(f"Error searching elevation data: {e}")
            raise
    
    def _select_best_feature(self, features: list) -> Dict[str, Any]:
        """Select the best feature from search results."""
        if not features:
            raise Exception("No features found in search results")
        
        # For now, return the first feature
        # In a more sophisticated implementation, we could rank by:
        # - Resolution
        # - Recency
        # - Coverage quality
        return features[0]
    
    async def _extract_elevation_value(
        self, 
        feature: Dict[str, Any], 
        latitude: float, 
        longitude: float
    ) -> Dict[str, Any]:
        """Extract elevation value from a STAC feature."""
        try:
            # Get the data asset URL
            assets = feature.get("assets", {})
            
            # Look for common elevation data asset names
            data_asset = None
            for asset_name in ["data", "COG", "elevation", "dem"]:
                if asset_name in assets:
                    data_asset = assets[asset_name]
                    break
            
            if not data_asset:
                raise Exception("No elevation data asset found in feature")
            
            # Get the data URL
            data_url = data_asset.get("href")
            if not data_url:
                raise Exception("No data URL found in asset")
            
            # Read elevation value from the raster
            elevation_value = await self._read_raster_value(data_url, latitude, longitude)
            
            # Get additional metadata
            resolution = self._extract_resolution(feature)
            confidence = self._calculate_confidence(feature, latitude, longitude)
            
            return {
                "elevation_m": elevation_value,
                "resolution_m": resolution,
                "confidence_level": confidence,
                "asset_url": data_url,
                "feature_id": feature.get("id"),
                "properties": feature.get("properties", {})
            }
            
        except Exception as e:
            logger.error(f"Error extracting elevation value: {e}")
            raise
    
    async def _read_raster_value(
        self, 
        data_url: str, 
        latitude: float, 
        longitude: float
    ) -> float:
        """Read elevation value from a raster URL at given coordinates."""
        try:
            # Create a point geometry
            point = Point(longitude, latitude)
            
            # Open the raster dataset
            with rasterio.open(data_url) as dataset:
                # Transform coordinates to raster CRS if needed
                if dataset.crs != CRS.from_epsg(4326):
                    # Transform from WGS84 to dataset CRS
                    x, y = transform(
                        CRS.from_epsg(4326),  # Source CRS (WGS84)
                        dataset.crs,          # Target CRS
                        [longitude], [latitude]
                    )
                else:
                    x, y = [longitude], [latitude]
                
                # Sample the raster at the point
                values = list(dataset.sample([(x[0], y[0])]))
                
                if not values:
                    raise Exception("No data found at specified coordinates")
                
                elevation = float(values[0][0])
                
                # Handle NoData values
                if elevation == dataset.nodata or np.isnan(elevation):
                    raise Exception("NoData value at specified coordinates")
                
                return elevation
                
        except Exception as e:
            logger.error(f"Error reading raster value: {e}")
            raise Exception(f"Failed to read elevation from raster: {e}")
    
    def _extract_resolution(self, feature: Dict[str, Any]) -> Optional[float]:
        """Extract resolution information from feature."""
        properties = feature.get("properties", {})
        
        # Look for resolution in various possible fields
        resolution_fields = [
            "gsd", "resolution", "spatial_resolution", 
            "ground_sample_distance", "pixel_size"
        ]
        
        for field in resolution_fields:
            if field in properties:
                try:
                    return float(properties[field])
                except (ValueError, TypeError):
                    continue
        
        # Default resolution based on collection
        collection = feature.get("collection", "")
        if "GLO-30" in collection:
            return 30.0  # 30m resolution
        elif "HLSL30" in collection:
            return 30.0  # 30m resolution
        elif "ASTER" in collection:
            return 90.0  # 90m resolution
        elif "SRTM" in collection:
            return 90.0  # 90m resolution
        
        return None
    
    def _calculate_confidence(
        self, 
        feature: Dict[str, Any], 
        latitude: float, 
        longitude: float
    ) -> float:
        """Calculate confidence level for the elevation data."""
        try:
            # Base confidence
            confidence = 0.8
            
            # Check if point is within feature geometry
            geometry = feature.get("geometry")
            if geometry:
                point = Point(longitude, latitude)
                # This would require more sophisticated geometry checking
                # For now, assume high confidence
                confidence = 0.9
            
            # Adjust based on data quality indicators
            properties = feature.get("properties", {})
            
            # Check for quality flags
            if "quality" in properties:
                quality = properties["quality"]
                if quality == "high":
                    confidence += 0.1
                elif quality == "low":
                    confidence -= 0.2
            
            # Check for cloud coverage
            if "cloud_cover" in properties:
                cloud_cover = properties["cloud_cover"]
                if cloud_cover > 50:
                    confidence -= 0.2
                elif cloud_cover < 10:
                    confidence += 0.1
            
            # Ensure confidence is between 0 and 1
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            logger.warning(f"Error calculating confidence: {e}")
            return 0.7  # Default confidence
    
    async def get_available_collections(self) -> list:
        """Get list of available elevation data collections."""
        try:
            response = await self.session.get(f"{self.CMR_STAC_ENDPOINT}/collections")
            response.raise_for_status()
            
            collections_data = response.json()
            collections = collections_data.get("collections", [])
            
            # Filter for elevation-related collections
            elevation_collections = []
            for collection in collections:
                title = collection.get("title", "").lower()
                description = collection.get("description", "").lower()
                
                if any(keyword in title or keyword in description 
                      for keyword in ["elevation", "dem", "topography", "terrain"]):
                    elevation_collections.append({
                        "id": collection.get("id"),
                        "title": collection.get("title"),
                        "description": collection.get("description")
                    })
            
            return elevation_collections
            
        except Exception as e:
            logger.error(f"Error getting available collections: {e}")
            return self.ELEVATION_COLLECTIONS


# Example usage and testing
async def test_extractor():
    """Test function for the topography extractor."""
    async with TopographyExtractor() as extractor:
        try:
            # Test with coordinates in Colorado, USA
            data = await extractor.extract_elevation_data(39.7392, -104.9903)
            print("Extracted elevation data:")
            print(f"Elevation: {data['elevation_m']} m")
            print(f"Resolution: {data['resolution_m']} m")
            print(f"Confidence: {data['confidence_level']}")
            print(f"Data Source: {data['data_source']}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_extractor())