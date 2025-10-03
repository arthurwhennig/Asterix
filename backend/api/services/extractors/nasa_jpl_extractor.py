"""
NASA JPL Small-Body Database (SBDB) Extractor

This module extracts asteroid characteristics from NASA's JPL Small-Body Database API.
It retrieves diameter, velocity, and other physical parameters for impact simulation.
"""

import httpx
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class NASAJPLExtractor:
    """Extractor for NASA JPL Small-Body Database API."""
    
    BASE_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def extract_asteroid_data(self, asteroid_name: str) -> Dict[str, Any]:
        """
        Extract asteroid data from NASA JPL SBDB API.
        
        Args:
            asteroid_name: Name or designation of the asteroid (e.g., "Apophis", "Bennu")
            
        Returns:
            Dictionary containing extracted asteroid data
            
        Raises:
            Exception: If API call fails or data cannot be parsed
        """
        try:
            # Construct API request URL
            url = self._construct_api_url(asteroid_name)
            
            # Make API request
            response = await self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse and validate response
            asteroid_data = self._parse_response(data, asteroid_name)
            
            logger.info(f"Successfully extracted data for asteroid: {asteroid_name}")
            return asteroid_data
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while extracting data for {asteroid_name}: {e}")
            raise Exception(f"Failed to fetch data from NASA JPL API: {e}")
        except Exception as e:
            logger.error(f"Error extracting asteroid data for {asteroid_name}: {e}")
            raise
    
    def _construct_api_url(self, asteroid_name: str) -> str:
        """Construct the API URL with required parameters."""
        params = {
            "sstr": asteroid_name,
            "phys-par": "1",  # Request physical parameters
            "ca-data": "1"    # Request close-approach data
        }
        
        # Build query string
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.BASE_URL}?{query_string}"
    
    def _parse_response(self, data: Dict[str, Any], asteroid_name: str) -> Dict[str, Any]:
        """
        Parse the JSON response from NASA JPL API.
        
        Args:
            data: Raw JSON response from API
            asteroid_name: Name of the asteroid for error reporting
            
        Returns:
            Parsed asteroid data dictionary
            
        Raises:
            Exception: If required data is missing or invalid
        """
        try:
            # Extract basic information
            object_data = data.get("object", {})
            if not object_data:
                raise Exception("No object data found in API response")
            
            # Extract physical parameters
            phys_par = data.get("phys_par", {})
            if not phys_par:
                raise Exception("No physical parameters found in API response")
            
            # Extract close-approach data
            ca_data = data.get("ca_data", [])
            if not ca_data:
                raise Exception("No close-approach data found in API response")
            
            # Extract diameter (convert from km to meters)
            diameter_km = None
            diameter_str = phys_par.get("diameter")
            if diameter_str:
                try:
                    diameter_km = float(diameter_str)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid diameter value: {diameter_str}")
            
            diameter_m = diameter_km * 1000 if diameter_km else None
            
            # Extract velocity (convert from km/s to m/s)
            velocity_ms = None
            if ca_data:
                # Use the most recent close-approach data
                latest_ca = ca_data[0]
                velocity_str = latest_ca.get("v_rel")
                if velocity_str:
                    try:
                        velocity_km_s = float(velocity_str)
                        velocity_ms = velocity_km_s * 1000
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid velocity value: {velocity_str}")
            
            # Extract mass if available
            mass_kg = None
            mass_str = phys_par.get("mass")
            if mass_str:
                try:
                    # Mass is typically in kg, but check if conversion is needed
                    mass_kg = float(mass_str)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid mass value: {mass_str}")
            
            # Extract composition
            composition = phys_par.get("spec_B", "Unknown")
            
            # Extract orbital data
            orbital_data = {
                "semi_major_axis": object_data.get("a"),
                "eccentricity": object_data.get("e"),
                "inclination": object_data.get("i"),
                "longitude_of_ascending_node": object_data.get("om"),
                "argument_of_perihelion": object_data.get("w"),
                "mean_anomaly": object_data.get("ma"),
                "orbital_period": object_data.get("per"),
            }
            
            # Extract close-approach data
            close_approach_data = []
            for ca in ca_data[:5]:  # Limit to 5 most recent approaches
                close_approach_data.append({
                    "date": ca.get("date"),
                    "distance_km": ca.get("dist"),
                    "velocity_km_s": ca.get("v_rel"),
                    "body": ca.get("body")
                })
            
            # Check if potentially hazardous
            is_potentially_hazardous = object_data.get("pha", "N") == "Y"
            
            # Validate required data
            if diameter_m is None:
                raise Exception("Asteroid diameter could not be extracted")
            if velocity_ms is None:
                raise Exception("Asteroid velocity could not be extracted")
            
            return {
                "name": asteroid_name,
                "nasa_id": object_data.get("des", asteroid_name),
                "diameter_m": diameter_m,
                "velocity_ms": velocity_ms,
                "mass_kg": mass_kg,
                "composition": composition,
                "orbital_data": orbital_data,
                "close_approach_data": close_approach_data,
                "is_potentially_hazardous": is_potentially_hazardous,
                "extracted_at": datetime.utcnow().isoformat(),
                "data_source": "NASA JPL SBDB",
                "api_version": data.get("signature", {}).get("version", "Unknown")
            }
            
        except Exception as e:
            logger.error(f"Error parsing NASA JPL response for {asteroid_name}: {e}")
            raise Exception(f"Failed to parse asteroid data: {e}")
    
    async def get_asteroid_list(self, limit: int = 100) -> list:
        """
        Get a list of asteroids from NASA JPL API.
        
        Args:
            limit: Maximum number of asteroids to return
            
        Returns:
            List of asteroid names and basic info
        """
        try:
            # This would require a different endpoint or approach
            # For now, return a list of well-known asteroids
            well_known_asteroids = [
                "Apophis",
                "Bennu",
                "Didymos",
                "Eros",
                "Gaspra",
                "Ida",
                "Mathilde",
                "Vesta",
                "Ceres",
                "Pallas"
            ]
            
            return well_known_asteroids[:limit]
            
        except Exception as e:
            logger.error(f"Error getting asteroid list: {e}")
            raise


# Example usage and testing
async def test_extractor():
    """Test function for the NASA JPL extractor."""
    async with NASAJPLExtractor() as extractor:
        try:
            # Test with Apophis
            data = await extractor.extract_asteroid_data("Apophis")
            print("Extracted data for Apophis:")
            print(f"Diameter: {data['diameter_m']} m")
            print(f"Velocity: {data['velocity_ms']} m/s")
            print(f"Mass: {data['mass_kg']} kg")
            print(f"Composition: {data['composition']}")
            print(f"Potentially Hazardous: {data['is_potentially_hazardous']}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_extractor())