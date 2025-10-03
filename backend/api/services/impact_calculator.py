"""
Impact Calculator Service

This module implements impact calculations using kinetic energy formulas and USGS data
to model secondary consequences of meteor impacts including craters, airblast effects,
earthquakes, and tsunamis.
"""

import logging
import math
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


class ImpactCalculator:
    """Calculator for asteroid impact effects and secondary consequences."""
    
    # Physical constants
    EARTH_RADIUS = 6371000  # meters
    EARTH_MASS = 5.972e24  # kg
    GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/kg/s²
    
    # Energy conversion factors
    JOULES_TO_MEGATONS = 1 / (4.184e15)  # 1 megaton TNT = 4.184e15 J
    
    # Default asteroid properties
    DEFAULT_ASTEROID_DENSITY = 3000  # kg/m³ (typical stony asteroid)
    DEFAULT_TARGET_DENSITY = 2500  # kg/m³ (typical Earth surface)
    
    # Damage thresholds (PSI)
    DAMAGE_THRESHOLDS = {
        "window_shatter": 1.0,
        "residential_damage": 2.5,
        "building_destruction": 5.0,
        "concrete_damage": 15.0
    }
    
    def __init__(self):
        pass
    
    def calculate_impact_effects(
        self,
        asteroid_diameter_m: float,
        asteroid_velocity_ms: float,
        asteroid_density_kg_m3: float,
        target_density_kg_m3: float,
        impact_latitude: float,
        impact_longitude: float,
        elevation_m: float,
        is_land: bool,
        water_depth_m: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive impact effects.
        
        Args:
            asteroid_diameter_m: Asteroid diameter in meters
            asteroid_velocity_ms: Asteroid velocity in m/s
            asteroid_density_kg_m3: Asteroid density in kg/m³
            target_density_kg_m3: Target surface density in kg/m³
            impact_latitude: Impact latitude in decimal degrees
            impact_longitude: Impact longitude in decimal degrees
            elevation_m: Ground elevation in meters
            is_land: Whether impact is on land (True) or water (False)
            water_depth_m: Water depth in meters (if not on land)
            
        Returns:
            Dictionary containing calculated impact effects
        """
        try:
            # Calculate basic impact parameters
            impact_energy = self._calculate_kinetic_energy(
                asteroid_diameter_m, asteroid_velocity_ms, asteroid_density_kg_m3
            )
            
            # Calculate crater dimensions
            crater_data = self._calculate_crater_dimensions(
                asteroid_diameter_m, asteroid_density_kg_m3, 
                target_density_kg_m3, impact_energy
            )
            
            # Calculate airblast effects
            airblast_data = self._calculate_airblast_effects(impact_energy)
            
            # Calculate earthquake effects
            earthquake_data = self._calculate_earthquake_effects(impact_energy)
            
            # Calculate thermal effects
            thermal_data = self._calculate_thermal_effects(impact_energy)
            
            # Calculate tsunami effects (if applicable)
            tsunami_data = None
            if not is_land:
                tsunami_data = self._calculate_tsunami_effects(
                    crater_data["diameter_km"], water_depth_m
                )
            
            # Calculate damage zones
            damage_zones = self._calculate_damage_zones(airblast_data)
            
            # Combine all results
            impact_results = {
                "impact_energy": {
                    "joules": impact_energy,
                    "megatons_tnt": impact_energy * self.JOULES_TO_MEGATONS,
                    "kilotons_tnt": impact_energy * self.JOULES_TO_MEGATONS * 1000
                },
                "crater": crater_data,
                "airblast": airblast_data,
                "earthquake": earthquake_data,
                "thermal": thermal_data,
                "tsunami": tsunami_data,
                "damage_zones": damage_zones,
                "impact_location": {
                    "latitude": impact_latitude,
                    "longitude": impact_longitude,
                    "elevation_m": elevation_m,
                    "is_land": is_land,
                    "water_depth_m": water_depth_m
                },
                "calculated_at": datetime.utcnow().isoformat(),
                "calculation_method": "simplified_scaling_laws"
            }
            
            logger.info(f"Calculated impact effects for {asteroid_diameter_m}m asteroid")
            return impact_results
            
        except Exception as e:
            logger.error(f"Error calculating impact effects: {e}")
            raise
    
    def _calculate_kinetic_energy(
        self, 
        diameter_m: float, 
        velocity_ms: float, 
        density_kg_m3: float
    ) -> float:
        """Calculate kinetic energy of the impactor."""
        try:
            # Calculate radius and volume
            radius_m = diameter_m / 2.0
            volume_m3 = (4.0 / 3.0) * math.pi * (radius_m ** 3)
            
            # Calculate mass
            mass_kg = density_kg_m3 * volume_m3
            
            # Calculate kinetic energy
            kinetic_energy = 0.5 * mass_kg * (velocity_ms ** 2)
            
            return kinetic_energy
            
        except Exception as e:
            logger.error(f"Error calculating kinetic energy: {e}")
            raise
    
    def _calculate_crater_dimensions(
        self,
        diameter_m: float,
        asteroid_density_kg_m3: float,
        target_density_kg_m3: float,
        kinetic_energy: float
    ) -> Dict[str, float]:
        """Calculate crater dimensions using Holsapple-Schmidt scaling law."""
        try:
            # Target melting energy (approximate)
            target_melting_energy = 2.5e6  # J/kg (typical for rock)
            
            # Holsapple-Schmidt scaling law
            # D_c = 1.161 * (ρ_i/ρ_t)^(1/3) * (KE/E_m)^(0.22) * D_i
            density_ratio = asteroid_density_kg_m3 / target_density_kg_m3
            energy_ratio = kinetic_energy / (target_melting_energy * target_density_kg_m3)
            
            crater_diameter_m = (
                1.161 * 
                (density_ratio ** (1.0/3.0)) * 
                (energy_ratio ** 0.22) * 
                diameter_m
            )
            
            # Convert to kilometers
            crater_diameter_km = crater_diameter_m / 1000.0
            
            # Estimate crater depth (typically 1/5 to 1/3 of diameter)
            crater_depth_km = crater_diameter_km * 0.25
            
            return {
                "diameter_km": crater_diameter_km,
                "depth_km": crater_depth_km,
                "diameter_m": crater_diameter_m,
                "depth_m": crater_depth_km * 1000.0
            }
            
        except Exception as e:
            logger.error(f"Error calculating crater dimensions: {e}")
            raise
    
    def _calculate_airblast_effects(self, kinetic_energy: float) -> Dict[str, Any]:
        """Calculate airblast effects and overpressure zones."""
        try:
            # Calculate blast wave radius for different overpressure levels
            overpressure_levels = [1.0, 2.5, 5.0, 15.0]  # PSI
            blast_radii = {}
            
            for psi in overpressure_levels:
                # Overpressure formula: P = 0.85 * (KE)^(1/3) / r + 3 * (KE)^(2/3) / r² + 7 * (KE) / r³
                # Solve for r using numerical methods
                radius_km = self._solve_overpressure_radius(kinetic_energy, psi)
                blast_radii[f"{psi}_psi"] = radius_km
            
            # Calculate fireball radius
            fireball_radius_km = (kinetic_energy ** (1.0/3.0)) / 1000.0
            
            return {
                "blast_radii_km": blast_radii,
                "fireball_radius_km": fireball_radius_km,
                "overpressure_levels_psi": overpressure_levels
            }
            
        except Exception as e:
            logger.error(f"Error calculating airblast effects: {e}")
            raise
    
    def _solve_overpressure_radius(self, kinetic_energy: float, target_psi: float) -> float:
        """Solve for radius at given overpressure level using numerical methods."""
        try:
            # Convert PSI to Pascals
            target_pressure_pa = target_psi * 6894.76
            
            # Use Newton's method to solve the overpressure equation
            # P = 0.85 * (KE)^(1/3) / r + 3 * (KE)^(2/3) / r² + 7 * (KE) / r³
            
            # Initial guess
            r = 1000.0  # meters
            
            for _ in range(100):  # Maximum iterations
                # Calculate pressure at current radius
                pressure = (
                    0.85 * (kinetic_energy ** (1.0/3.0)) / r +
                    3.0 * (kinetic_energy ** (2.0/3.0)) / (r ** 2) +
                    7.0 * kinetic_energy / (r ** 3)
                )
                
                # Calculate derivative
                dP_dr = (
                    -0.85 * (kinetic_energy ** (1.0/3.0)) / (r ** 2) -
                    6.0 * (kinetic_energy ** (2.0/3.0)) / (r ** 3) -
                    21.0 * kinetic_energy / (r ** 4)
                )
                
                # Newton's method update
                r_new = r - (pressure - target_pressure_pa) / dP_dr
                
                # Check convergence
                if abs(r_new - r) < 1.0:  # 1 meter tolerance
                    break
                
                r = r_new
            
            # Convert to kilometers
            return r / 1000.0
            
        except Exception as e:
            logger.error(f"Error solving overpressure radius: {e}")
            # Return a default value based on energy
            return (kinetic_energy ** (1.0/3.0)) / 1000.0
    
    def _calculate_earthquake_effects(self, kinetic_energy: float) -> Dict[str, Any]:
        """Calculate earthquake effects using moment magnitude."""
        try:
            # Calculate moment magnitude
            # M_w = 0.67 * log_10(KE) - 5.87
            moment_magnitude = 0.67 * math.log10(kinetic_energy) - 5.87
            
            # Calculate Richter magnitude (approximate)
            richter_magnitude = moment_magnitude - 0.2
            
            # Estimate shaking intensity at different distances
            # This is a simplified model
            distances_km = [10, 50, 100, 500, 1000]
            shaking_intensities = {}
            
            for distance in distances_km:
                # Simplified intensity calculation
                intensity = max(1, moment_magnitude - math.log10(distance) - 1.0)
                shaking_intensities[f"{distance}_km"] = min(12, max(1, intensity))
            
            return {
                "moment_magnitude": moment_magnitude,
                "richter_magnitude": richter_magnitude,
                "shaking_intensities": shaking_intensities,
                "distances_km": distances_km
            }
            
        except Exception as e:
            logger.error(f"Error calculating earthquake effects: {e}")
            raise
    
    def _calculate_thermal_effects(self, kinetic_energy: float) -> Dict[str, Any]:
        """Calculate thermal radiation effects."""
        try:
            # Calculate thermal radiation radius
            # This is a simplified model
            thermal_radius_km = (kinetic_energy ** (1.0/3.0)) / 2000.0
            
            # Calculate fireball temperature (approximate)
            fireball_temperature_k = 3000 + (kinetic_energy ** (1.0/4.0)) / 1000.0
            
            return {
                "thermal_radius_km": thermal_radius_km,
                "fireball_temperature_k": fireball_temperature_k,
                "fireball_temperature_c": fireball_temperature_k - 273.15
            }
            
        except Exception as e:
            logger.error(f"Error calculating thermal effects: {e}")
            raise
    
    def _calculate_tsunami_effects(
        self, 
        crater_diameter_km: float, 
        water_depth_m: float
    ) -> Dict[str, Any]:
        """Calculate tsunami effects for water impacts."""
        try:
            if water_depth_m <= 0:
                return None
            
            # Tsunami wave height formula
            # H = 0.15 * ((D_c^4) / (d^2 * r^2))^(1/4)
            # where D_c is crater diameter, d is water depth, r is distance
            
            # Calculate initial wave height at impact site
            initial_wave_height_m = 0.15 * (
                (crater_diameter_km ** 4) / 
                ((water_depth_m / 1000.0) ** 2)
            ) ** (1.0/4.0)
            
            # Calculate wave heights at different distances
            distances_km = [10, 50, 100, 500, 1000]
            wave_heights = {}
            
            for distance in distances_km:
                wave_height = 0.15 * (
                    (crater_diameter_km ** 4) / 
                    ((water_depth_m / 1000.0) ** 2 * (distance ** 2))
                ) ** (1.0/4.0)
                
                wave_heights[f"{distance}_km"] = max(0.1, wave_height)
            
            return {
                "initial_wave_height_m": initial_wave_height_m,
                "wave_heights": wave_heights,
                "distances_km": distances_km,
                "water_depth_m": water_depth_m
            }
            
        except Exception as e:
            logger.error(f"Error calculating tsunami effects: {e}")
            raise
    
    def _calculate_damage_zones(self, airblast_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate damage zones based on overpressure levels."""
        try:
            blast_radii = airblast_data.get("blast_radii_km", {})
            
            damage_zones = {}
            
            # Window shatter zone
            if "1.0_psi" in blast_radii:
                damage_zones["window_shatter"] = {
                    "radius_km": blast_radii["1.0_psi"],
                    "description": "Most windows shatter",
                    "damage_level": "light"
                }
            
            # Residential damage zone
            if "2.5_psi" in blast_radii:
                damage_zones["residential_damage"] = {
                    "radius_km": blast_radii["2.5_psi"],
                    "description": "Most residential buildings severely damaged",
                    "damage_level": "moderate"
                }
            
            # Building destruction zone
            if "5.0_psi" in blast_radii:
                damage_zones["building_destruction"] = {
                    "radius_km": blast_radii["5.0_psi"],
                    "description": "Most buildings destroyed",
                    "damage_level": "severe"
                }
            
            # Concrete damage zone
            if "15.0_psi" in blast_radii:
                damage_zones["concrete_damage"] = {
                    "radius_km": blast_radii["15.0_psi"],
                    "description": "Reinforced concrete buildings severely damaged",
                    "damage_level": "extreme"
                }
            
            return damage_zones
            
        except Exception as e:
            logger.error(f"Error calculating damage zones: {e}")
            raise
    
    def estimate_impact_energy_from_diameter(
        self, 
        diameter_m: float, 
        velocity_ms: float = 17000.0,
        density_kg_m3: float = None
    ) -> float:
        """Estimate impact energy from asteroid diameter."""
        if density_kg_m3 is None:
            density_kg_m3 = self.DEFAULT_ASTEROID_DENSITY
        
        return self._calculate_kinetic_energy(diameter_m, velocity_ms, density_kg_m3)
    
    def get_impact_comparison(self, kinetic_energy: float) -> Dict[str, Any]:
        """Get comparison with known historical impacts."""
        comparisons = {
            "tunguska": {
                "energy_joules": 3.0e15,  # ~15 megatons
                "description": "Tunguska event (1908)"
            },
            "chicxulub": {
                "energy_joules": 1.3e23,  # ~65 billion megatons
                "description": "Chicxulub impact (K-T boundary)"
            },
            "hiroshima": {
                "energy_joules": 6.3e13,  # ~15 kilotons
                "description": "Hiroshima atomic bomb"
            },
            "tsar_bomba": {
                "energy_joules": 2.1e17,  # ~50 megatons
                "description": "Tsar Bomba (largest nuclear test)"
            }
        }
        
        # Find closest comparison
        closest_comparison = None
        min_ratio = float('inf')
        
        for name, comparison in comparisons.items():
            ratio = abs(math.log10(kinetic_energy / comparison["energy_joules"]))
            if ratio < min_ratio:
                min_ratio = ratio
                closest_comparison = {
                    "name": name,
                    "energy_joules": comparison["energy_joules"],
                    "description": comparison["description"],
                    "ratio": kinetic_energy / comparison["energy_joules"]
                }
        
        return closest_comparison


# Example usage and testing
def test_calculator():
    """Test function for the impact calculator."""
    calculator = ImpactCalculator()
    
    try:
        # Test with a 100m diameter asteroid
        results = calculator.calculate_impact_effects(
            asteroid_diameter_m=100.0,
            asteroid_velocity_ms=17000.0,
            asteroid_density_kg_m3=3000.0,
            target_density_kg_m3=2500.0,
            impact_latitude=39.7392,
            impact_longitude=-104.9903,
            elevation_m=1600.0,
            is_land=True
        )
        
        print("Impact calculation results:")
        print(f"Energy: {results['impact_energy']['megatons_tnt']:.2f} megatons TNT")
        print(f"Crater diameter: {results['crater']['diameter_km']:.2f} km")
        print(f"Fireball radius: {results['airblast']['fireball_radius_km']:.2f} km")
        print(f"Earthquake magnitude: {results['earthquake']['moment_magnitude']:.2f}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_calculator()
