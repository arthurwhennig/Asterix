"""
NASA JPL Small-Body Database (SBDB) and Horizons API Extractor

This module extracts asteroid characteristics from NASA's JPL Small-Body Database API
and trajectory data from NASA's JPL Horizons API. It retrieves diameter, velocity,
and other physical parameters for impact simulation, as well as ephemeris data for
trajectory analysis.
"""

import httpx
import logging
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timedelta
import asyncio
import re

logger = logging.getLogger(__name__)


class NASAJPLExtractor:
    """Extractor for NASA JPL Small-Body Database API and Horizons API."""

    SBDB_BASE_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"
    HORIZONS_BASE_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

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
            url = self._construct_sbdb_api_url(asteroid_name)

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

    async def extract_asteroid_trajectory(
        self,
        asteroid_id: str,
        start_time: str,
        stop_time: str,
        step_size: str = "1d",
        center: str = "500@0",
    ) -> Dict[str, Any]:
        """
        Extract asteroid trajectory data from NASA JPL Horizons API.

        Args:
            asteroid_id: NASA ID or designation of the asteroid (e.g., "2000433" for 433 Eros)
            start_time: Start time for trajectory data (format: "YYYY-MM-DD")
            stop_time: Stop time for trajectory data (format: "YYYY-MM-DD")
            step_size: Time step between data points (e.g., "1d", "1h", "30m")
            center: Coordinate center reference (default: "500@0" for solar system barycenter)

        Returns:
            Dictionary containing trajectory data with position and velocity vectors

        Raises:
            Exception: If API call fails or data cannot be parsed
        """
        try:
            # Construct API request URL
            url = self._construct_horizons_api_url(
                asteroid_id, start_time, stop_time, step_size, center
            )

            # Make API request
            response = await self.session.get(url)
            response.raise_for_status()

            # Parse the text response
            trajectory_data = self._parse_horizons_response(response.text, asteroid_id)

            logger.info(
                f"Successfully extracted trajectory data for asteroid: {asteroid_id}"
            )
            return trajectory_data

        except httpx.HTTPError as e:
            logger.error(
                f"HTTP error while extracting trajectory for {asteroid_id}: {e}"
            )
            raise Exception(
                f"Failed to fetch trajectory data from NASA JPL Horizons API: {e}"
            )
        except Exception as e:
            logger.error(f"Error extracting trajectory data for {asteroid_id}: {e}")
            raise

    def _construct_sbdb_api_url(self, asteroid_name: str) -> str:
        """Construct the SBDB API URL with required parameters."""
        params = {
            "sstr": asteroid_name,
            "phys-par": "1",  # Request physical parameters
            "ca-data": "1"    # Request close-approach data
        }

        # Build query string
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.SBDB_BASE_URL}?{query_string}"

    def _construct_horizons_api_url(
        self,
        asteroid_id: str,
        start_time: str,
        stop_time: str,
        step_size: str = "1d",
        center: str = "500@0",
    ) -> str:
        """Construct the Horizons API URL with required parameters."""
        params = {
            "format": "text",
            "COMMAND": f"'{asteroid_id}'",
            "OBJ_DATA": "YES",
            "MAKE_EPHEM": "YES",
            "EPHEM_TYPE": "VECTORS",
            "CENTER": f"'{center}'",
            "START_TIME": f"'{start_time}'",
            "STOP_TIME": f"'{stop_time}'",
            "STEP_SIZE": f"'{step_size}'",
        }

        # Build query string
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        return f"{self.HORIZONS_BASE_URL}?{query_string}"

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

    def _parse_horizons_response(
        self, response_text: str, asteroid_id: str
    ) -> Dict[str, Any]:
        """
        Parse the text response from NASA JPL Horizons API.

        Args:
            response_text: Raw text response from Horizons API
            asteroid_id: ID of the asteroid for error reporting

        Returns:
            Parsed trajectory data dictionary

        Raises:
            Exception: If required data is missing or invalid
        """
        try:
            # Find the start and end of ephemeris data
            soe_start = response_text.find("$$SOE")
            eoe_end = response_text.find("$$EOE")

            if soe_start == -1 or eoe_end == -1:
                raise Exception("Could not find ephemeris data markers ($$SOE/$$EOE)")

            # Extract the ephemeris data section
            ephemeris_section = response_text[soe_start:eoe_end]

            # Parse metadata from the header
            metadata = self._parse_horizons_metadata(response_text[:soe_start])

            # Parse the ephemeris data lines
            trajectory_points = self._parse_ephemeris_data(ephemeris_section)

            if not trajectory_points:
                raise Exception("No trajectory data points found in response")

            return {
                "asteroid_id": asteroid_id,
                "metadata": metadata,
                "trajectory_points": trajectory_points,
                "data_points_count": len(trajectory_points),
                "extracted_at": datetime.utcnow().isoformat(),
                "data_source": "NASA JPL Horizons",
                "coordinate_system": metadata.get("coordinate_system", "Unknown"),
            }

        except Exception as e:
            logger.error(f"Error parsing Horizons response for {asteroid_id}: {e}")
            raise Exception(f"Failed to parse trajectory data: {e}")

    def _parse_horizons_metadata(self, header_text: str) -> Dict[str, Any]:
        """Parse metadata from the Horizons API response header."""
        metadata = {}

        # Extract coordinate system
        coord_match = re.search(r"Coordinate system\s*:\s*(.+)", header_text)
        if coord_match:
            metadata["coordinate_system"] = coord_match.group(1).strip()

        # Extract reference frame
        frame_match = re.search(r"Reference frame\s*:\s*(.+)", header_text)
        if frame_match:
            metadata["reference_frame"] = frame_match.group(1).strip()

        # Extract target object info
        target_match = re.search(r"Target body name\s*:\s*(.+)", header_text)
        if target_match:
            metadata["target_name"] = target_match.group(1).strip()

        return metadata

    def _parse_ephemeris_data(self, ephemeris_section: str) -> List[Dict[str, Any]]:
        """Parse the ephemeris data section into structured trajectory points."""
        trajectory_points = []

        lines = ephemeris_section.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("$$SOE"):
                continue

            # Parse the ephemeris data line
            # Format: JDCT X Y Z VX VY VZ LT RG RR
            parts = line.split()

            if len(parts) >= 7:
                try:
                    # Extract Julian Date and position/velocity vectors
                    julian_date = float(parts[0])
                    x = float(parts[1])  # Position X (km)
                    y = float(parts[2])  # Position Y (km)
                    z = float(parts[3])  # Position Z (km)
                    vx = float(parts[4])  # Velocity X (km/s)
                    vy = float(parts[5])  # Velocity Y (km/s)
                    vz = float(parts[6])  # Velocity Z (km/s)

                    # Calculate magnitude of position and velocity
                    position_magnitude = (x**2 + y**2 + z**2) ** 0.5
                    velocity_magnitude = (vx**2 + vy**2 + vz**2) ** 0.5

                    trajectory_points.append(
                        {
                            "julian_date": julian_date,
                            "position": {
                                "x_km": x,
                                "y_km": y,
                                "z_km": z,
                                "magnitude_km": position_magnitude,
                            },
                            "velocity": {
                                "x_km_s": vx,
                                "y_km_s": vy,
                                "z_km_s": vz,
                                "magnitude_km_s": velocity_magnitude,
                            },
                        }
                    )

                except (ValueError, IndexError) as e:
                    logger.warning(f"Failed to parse ephemeris line: {line} - {e}")
                    continue

        return trajectory_points

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
            # Test with Apophis - basic data
            print("=== Testing SBDB Data Extraction ===")
            data = await extractor.extract_asteroid_data("Apophis")
            print("Extracted data for Apophis:")
            print(f"Diameter: {data['diameter_m']} m")
            print(f"Velocity: {data['velocity_ms']} m/s")
            print(f"Mass: {data['mass_kg']} kg")
            print(f"Composition: {data['composition']}")
            print(f"Potentially Hazardous: {data['is_potentially_hazardous']}")
            print()

            # Test trajectory extraction for 433 Eros
            print("=== Testing Horizons Trajectory Extraction ===")
            trajectory = await extractor.extract_asteroid_trajectory(
                asteroid_id="2000433",  # 433 Eros
                start_time="2025-01-01",
                stop_time="2025-01-10",
                step_size="1d",
            )

            print(f"Trajectory data for asteroid {trajectory['asteroid_id']}:")
            print(f"Data points: {trajectory['data_points_count']}")
            print(f"Coordinate system: {trajectory['coordinate_system']}")
            print(
                f"Target name: {trajectory['metadata'].get('target_name', 'Unknown')}"
            )

            # Show first few trajectory points
            print("\nFirst 3 trajectory points:")
            for i, point in enumerate(trajectory["trajectory_points"][:3]):
                print(f"  Point {i+1}:")
                print(f"    Julian Date: {point['julian_date']}")
                print(
                    f"    Position: ({point['position']['x_km']:.2f}, {point['position']['y_km']:.2f}, {point['position']['z_km']:.2f}) km"
                )
                print(
                    f"    Position magnitude: {point['position']['magnitude_km']:.2f} km"
                )
                print(
                    f"    Velocity: ({point['velocity']['x_km_s']:.2f}, {point['velocity']['y_km_s']:.2f}, {point['velocity']['z_km_s']:.2f}) km/s"
                )
                print(
                    f"    Velocity magnitude: {point['velocity']['magnitude_km_s']:.2f} km/s"
                )

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_extractor())
