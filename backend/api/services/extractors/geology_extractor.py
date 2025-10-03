"""
OneGeology Geological Data Extractor

This module extracts geological data from OneGeology WFS services to determine
surface material type and density for impact simulation calculations.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import httpx
import xml.etree.ElementTree as ET
import json
import math
from shapely.geometry import Point
from shapely.wkt import loads

logger = logging.getLogger(__name__)


class GeologyExtractor:
    """Extractor for geological data from OneGeology WFS services."""
    
    # Regional WFS endpoints for different geological surveys
    WFS_ENDPOINTS = {
        "USGS": {
            "url": "https://mrdata.usgs.gov/services/wfs/geology",
            "layer": "usgeol",
            "description_field": "ROCK_D",
            "name_field": "UNIT_NAME"
        },
        "BGS": {
            "url": "https://ogc.bgs.ac.uk/cgi-bin/BGS_Bedrock_and_Superficial_Geology/wfs",
            "layer": "BGS_Bedrock_and_Superficial_Geology",
            "description_field": "DESCRIPTION",
            "name_field": "UNIT_NAME"
        },
        "Geological_Survey_of_Canada": {
            "url": "https://gdr.agg.nrcan.gc.ca/geoserver/wfs",
            "layer": "CGU",
            "description_field": "UNIT_DESC",
            "name_field": "UNIT_NAME"
        }
    }
    
    # Density mapping for different rock types
    DENSITY_MAPPING = {
        # Igneous rocks
        "granite": 2750,
        "basalt": 2850,
        "gabbro": 2950,
        "diorite": 2800,
        "rhyolite": 2700,
        "andesite": 2750,
        "obsidian": 2600,
        "pumice": 1000,
        
        # Sedimentary rocks
        "sandstone": 2400,
        "limestone": 2700,
        "shale": 2600,
        "conglomerate": 2500,
        "breccia": 2500,
        "siltstone": 2600,
        "mudstone": 2600,
        "coal": 1400,
        
        # Metamorphic rocks
        "gneiss": 2750,
        "schist": 2700,
        "slate": 2750,
        "marble": 2700,
        "quartzite": 2650,
        "phyllite": 2700,
        
        # Unconsolidated materials
        "sand": 1600,
        "clay": 1800,
        "silt": 1700,
        "gravel": 1900,
        "soil": 1500,
        "loam": 1400,
        
        # Water and ice
        "water": 1000,
        "ice": 920,
        
        # Default values
        "unknown": 2500,
        "mixed": 2400
    }
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def extract_geological_data(
        self, 
        latitude: float, 
        longitude: float,
        region: str = "USGS"
    ) -> Dict[str, Any]:
        """
        Extract geological data for given coordinates.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            region: Regional geological survey to query
            
        Returns:
            Dictionary containing geological data
            
        Raises:
            Exception: If data extraction fails
        """
        try:
            # Validate coordinates
            if not (-90 <= latitude <= 90):
                raise ValueError(f"Invalid latitude: {latitude}")
            if not (-180 <= longitude <= 180):
                raise ValueError(f"Invalid longitude: {longitude}")
            
            # Get WFS endpoint configuration
            if region not in self.WFS_ENDPOINTS:
                raise ValueError(f"Unknown region: {region}")
            
            endpoint_config = self.WFS_ENDPOINTS[region]
            
            # Query WFS service
            geological_data = await self._query_wfs_service(
                latitude, longitude, endpoint_config
            )
            
            # Map description to density
            density = self._map_description_to_density(
                geological_data.get("description", "")
            )
            
            # Add calculated fields
            geological_data.update({
                "latitude": latitude,
                "longitude": longitude,
                "density_kg_m3": density,
                "data_source": "OneGeology WFS",
                "region": region,
                "extracted_at": datetime.utcnow().isoformat()
            })
            
            logger.info(f"Successfully extracted geological data for ({latitude}, {longitude})")
            return geological_data
            
        except Exception as e:
            logger.error(f"Error extracting geological data for ({latitude}, {longitude}): {e}")
            raise
    
    async def _query_wfs_service(
        self, 
        latitude: float, 
        longitude: float, 
        endpoint_config: Dict[str, str]
    ) -> Dict[str, Any]:
        """Query WFS service for geological data."""
        try:
            # Create a small bounding box around the point
            bbox_size = 0.001  # degrees
            bbox = f"{longitude - bbox_size},{latitude - bbox_size},{longitude + bbox_size},{latitude + bbox_size}"
            
            # Construct WFS request parameters
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeName": endpoint_config["layer"],
                "BBOX": bbox,
                "outputFormat": "application/json",
                "srsName": "EPSG:4326"
            }
            
            # Make WFS request
            response = await self.session.get(
                endpoint_config["url"],
                params=params
            )
            response.raise_for_status()
            
            # Parse response
            if response.headers.get("content-type", "").startswith("application/json"):
                return self._parse_json_response(response.json(), endpoint_config)
            else:
                # Try to parse as XML/GML
                return self._parse_xml_response(response.text, endpoint_config)
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during WFS query: {e}")
            raise Exception(f"Failed to query WFS service: {e}")
        except Exception as e:
            logger.error(f"Error querying WFS service: {e}")
            raise
    
    def _parse_json_response(
        self, 
        response_data: Dict[str, Any], 
        endpoint_config: Dict[str, str]
    ) -> Dict[str, Any]:
        """Parse JSON response from WFS service."""
        try:
            features = response_data.get("features", [])
            
            if not features:
                return self._get_default_geological_data()
            
            # Get the first feature
            feature = features[0]
            properties = feature.get("properties", {})
            
            # Extract description and name
            description = properties.get(
                endpoint_config["description_field"], 
                "Unknown geological unit"
            )
            unit_name = properties.get(
                endpoint_config["name_field"], 
                "Unknown"
            )
            
            # Extract additional properties
            age_period = properties.get("AGE", properties.get("PERIOD", "Unknown"))
            formation_name = properties.get("FORMATION", properties.get("GROUP", unit_name))
            
            # Determine material type
            material_type = self._classify_material_type(description)
            
            return {
                "geological_description": str(description),
                "material_type": material_type,
                "age_period": str(age_period),
                "formation_name": str(formation_name),
                "unit_name": str(unit_name),
                "properties": properties
            }
            
        except Exception as e:
            logger.error(f"Error parsing JSON response: {e}")
            return self._get_default_geological_data()
    
    def _parse_xml_response(
        self, 
        response_text: str, 
        endpoint_config: Dict[str, str]
    ) -> Dict[str, Any]:
        """Parse XML/GML response from WFS service."""
        try:
            root = ET.fromstring(response_text)
            
            # Find feature elements
            features = root.findall(".//{http://www.opengis.net/gml/3.2}featureMember")
            
            if not features:
                return self._get_default_geological_data()
            
            # Get the first feature
            feature = features[0]
            
            # Extract properties based on namespace
            description = "Unknown geological unit"
            unit_name = "Unknown"
            age_period = "Unknown"
            formation_name = "Unknown"
            
            # Try to find description field
            for elem in feature.iter():
                if elem.tag.endswith(endpoint_config["description_field"]):
                    description = elem.text or "Unknown geological unit"
                elif elem.tag.endswith(endpoint_config["name_field"]):
                    unit_name = elem.text or "Unknown"
                elif elem.tag.endswith("AGE") or elem.tag.endswith("PERIOD"):
                    age_period = elem.text or "Unknown"
                elif elem.tag.endswith("FORMATION") or elem.tag.endswith("GROUP"):
                    formation_name = elem.text or unit_name
            
            # Determine material type
            material_type = self._classify_material_type(description)
            
            return {
                "geological_description": description,
                "material_type": material_type,
                "age_period": age_period,
                "formation_name": formation_name,
                "unit_name": unit_name,
                "properties": {}
            }
            
        except ET.ParseError as e:
            logger.error(f"Error parsing XML response: {e}")
            return self._get_default_geological_data()
        except Exception as e:
            logger.error(f"Error parsing XML response: {e}")
            return self._get_default_geological_data()
    
    def _classify_material_type(self, description: str) -> str:
        """Classify material type based on geological description."""
        if not description:
            return "unknown"
        
        description_lower = description.lower()
        
        # Check for specific rock types
        for rock_type in self.DENSITY_MAPPING.keys():
            if rock_type in description_lower:
                return rock_type
        
        # Check for general categories
        if any(word in description_lower for word in ["igneous", "volcanic", "plutonic"]):
            return "granite"  # Default igneous
        elif any(word in description_lower for word in ["sedimentary", "sandstone", "limestone"]):
            return "sandstone"  # Default sedimentary
        elif any(word in description_lower for word in ["metamorphic", "gneiss", "schist"]):
            return "gneiss"  # Default metamorphic
        elif any(word in description_lower for word in ["unconsolidated", "sand", "clay", "soil"]):
            return "sand"  # Default unconsolidated
        
        return "unknown"
    
    def _map_description_to_density(self, description: str) -> float:
        """Map geological description to density value."""
        if not description:
            return self.DENSITY_MAPPING["unknown"]
        
        description_lower = description.lower()
        
        # Check for exact matches first
        for rock_type, density in self.DENSITY_MAPPING.items():
            if rock_type in description_lower:
                return density
        
        # Check for general categories
        if any(word in description_lower for word in ["igneous", "volcanic", "plutonic"]):
            return self.DENSITY_MAPPING["granite"]
        elif any(word in description_lower for word in ["sedimentary", "sandstone", "limestone"]):
            return self.DENSITY_MAPPING["sandstone"]
        elif any(word in description_lower for word in ["metamorphic", "gneiss", "schist"]):
            return self.DENSITY_MAPPING["gneiss"]
        elif any(word in description_lower for word in ["unconsolidated", "sand", "clay", "soil"]):
            return self.DENSITY_MAPPING["sand"]
        
        return self.DENSITY_MAPPING["unknown"]
    
    def _get_default_geological_data(self) -> Dict[str, Any]:
        """Get default geological data when no specific data is found."""
        return {
            "geological_description": "Unknown geological unit",
            "material_type": "unknown",
            "age_period": "Unknown",
            "formation_name": "Unknown",
            "unit_name": "Unknown",
            "properties": {}
        }
    
    async def get_available_regions(self) -> List[Dict[str, str]]:
        """Get list of available regional geological surveys."""
        regions = []
        for region_id, config in self.WFS_ENDPOINTS.items():
            regions.append({
                "id": region_id,
                "url": config["url"],
                "layer": config["layer"],
                "description": f"{region_id} geological survey"
            })
        return regions


# Example usage and testing
async def test_extractor():
    """Test function for the geology extractor."""
    async with GeologyExtractor() as extractor:
        try:
            # Test with coordinates in Colorado, USA
            data = await extractor.extract_geological_data(39.7392, -104.9903, "USGS")
            print("Extracted geological data:")
            print(f"Description: {data['geological_description']}")
            print(f"Material Type: {data['material_type']}")
            print(f"Density: {data['density_kg_m3']} kg/m³")
            print(f"Age Period: {data['age_period']}")
            print(f"Formation: {data['formation_name']}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_extractor())