"""
Pydantic models for data extraction system.
These models define the structure of data extracted from various sources.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class CompositionType(str, Enum):
    """Asteroid composition types."""
    STONY = "stony"
    METALLIC = "metallic"
    CARBONACEOUS = "carbonaceous"
    ICY = "icy"
    MIXED = "mixed"


class GeologicalMaterial(str, Enum):
    """Common geological materials."""
    GRANITE = "granite"
    BASALT = "basalt"
    SANDSTONE = "sandstone"
    LIMESTONE = "limestone"
    CLAY = "clay"
    SAND = "sand"
    SHALE = "shale"
    MARBLE = "marble"
    QUARTZITE = "quartzite"
    GNEISS = "gneiss"
    SCHIST = "schist"
    SLATE = "slate"


class Coordinate(BaseModel):
    """Geographic coordinate."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    altitude: Optional[float] = Field(None, description="Altitude in meters")


class Vector3D(BaseModel):
    """3D vector representation."""
    x: float = Field(..., description="X coordinate in meters")
    y: float = Field(..., description="Y coordinate in meters")
    z: float = Field(..., description="Z coordinate in meters")


# 1. NASA JPL Asteroid Data Models
class NASAAsteroidData(BaseModel):
    """Asteroid data extracted from NASA JPL Small-Body Database."""
    name: str = Field(..., description="Asteroid name")
    nasa_id: str = Field(..., description="NASA asteroid designation")
    diameter_m: float = Field(..., gt=0, description="Diameter in meters")
    velocity_ms: float = Field(..., gt=0, description="Velocity in m/s")
    mass_kg: Optional[float] = Field(None, gt=0, description="Mass in kg")
    composition: Optional[CompositionType] = Field(None, description="Asteroid composition")
    orbital_data: Dict[str, Any] = Field(default_factory=dict, description="Orbital parameters")
    close_approach_data: List[Dict[str, Any]] = Field(default_factory=list, description="Close approach data")
    is_potentially_hazardous: bool = Field(False, description="Potentially hazardous flag")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


# 2. Topography/Elevation Data Models
class TopographyData(BaseModel):
    """Topography data extracted from NASA CMR."""
    coordinate: Coordinate = Field(..., description="Location coordinates")
    elevation_m: float = Field(..., description="Ground elevation in meters")
    data_source: str = Field(..., description="Data source (e.g., COP-DEM_GLO-30-DGED)")
    resolution_m: Optional[float] = Field(None, description="Data resolution in meters")
    confidence_level: Optional[float] = Field(None, ge=0, le=1, description="Data confidence level")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


# 3. Geological Data Models
class GeologicalData(BaseModel):
    """Geological data extracted from OneGeology WFS."""
    coordinate: Coordinate = Field(..., description="Location coordinates")
    geological_description: str = Field(..., description="Geological material description")
    material_type: Optional[GeologicalMaterial] = Field(None, description="Standardized material type")
    density_kg_m3: float = Field(..., gt=0, description="Target density in kg/m³")
    age_period: Optional[str] = Field(None, description="Geological age period")
    formation_name: Optional[str] = Field(None, description="Geological formation name")
    data_source: str = Field(..., description="WFS data source")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


# 4. Regional Data Models
class FaultData(BaseModel):
    """Fault line data."""
    name: str = Field(..., description="Fault name")
    distance_km: float = Field(..., ge=0, description="Distance to fault in km")
    fault_type: Optional[str] = Field(None, description="Type of fault")
    activity_status: Optional[str] = Field(None, description="Activity status")
    slip_rate: Optional[float] = Field(None, description="Slip rate in mm/year")


class BathymetryData(BaseModel):
    """Ocean depth data."""
    coordinate: Coordinate = Field(..., description="Location coordinates")
    depth_m: float = Field(..., description="Ocean depth in meters (negative for below sea level)")
    is_land: bool = Field(False, description="Whether location is on land")
    data_source: str = Field(..., description="Bathymetry data source")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


class PopulationData(BaseModel):
    """Population data within effect radius."""
    total_population: int = Field(..., ge=0, description="Total population count")
    population_density_km2: float = Field(..., ge=0, description="Population density per km²")
    affected_area_km2: float = Field(..., gt=0, description="Affected area in km²")
    major_cities: List[Dict[str, Any]] = Field(default_factory=list, description="Major cities in affected area")
    data_source: str = Field(..., description="Population data source")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


class InfrastructureData(BaseModel):
    """Infrastructure data within effect radius."""
    airports: List[Dict[str, Any]] = Field(default_factory=list, description="Airports in affected area")
    ports: List[Dict[str, Any]] = Field(default_factory=list, description="Ports in affected area")
    power_plants: List[Dict[str, Any]] = Field(default_factory=list, description="Power plants in affected area")
    hospitals: List[Dict[str, Any]] = Field(default_factory=list, description="Hospitals in affected area")
    schools: List[Dict[str, Any]] = Field(default_factory=list, description="Schools in affected area")
    data_source: str = Field(..., description="Infrastructure data source")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


class RegionalData(BaseModel):
    """Combined regional data."""
    coordinate: Coordinate = Field(..., description="Center coordinates")
    fault_data: Optional[FaultData] = Field(None, description="Nearest fault information")
    bathymetry_data: Optional[BathymetryData] = Field(None, description="Bathymetry information")
    population_data: Optional[PopulationData] = Field(None, description="Population information")
    infrastructure_data: Optional[InfrastructureData] = Field(None, description="Infrastructure information")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")


# Combined Impact Data Model
class ImpactData(BaseModel):
    """Complete impact data combining all extracted information."""
    asteroid_data: NASAAsteroidData = Field(..., description="Asteroid characteristics")
    impact_location: Coordinate = Field(..., description="Impact coordinates")
    topography_data: Optional[TopographyData] = Field(None, description="Topography at impact site")
    geological_data: Optional[GeologicalData] = Field(None, description="Geology at impact site")
    regional_data: Optional[RegionalData] = Field(None, description="Regional data around impact site")
    
    # Calculated impact parameters
    impact_energy_joules: Optional[float] = Field(None, gt=0, description="Calculated impact energy")
    impact_energy_megatons: Optional[float] = Field(None, gt=0, description="Impact energy in megatons TNT")
    crater_diameter_km: Optional[float] = Field(None, gt=0, description="Estimated crater diameter")
    crater_depth_km: Optional[float] = Field(None, gt=0, description="Estimated crater depth")
    
    extraction_metadata: Dict[str, Any] = Field(default_factory=dict, description="Extraction process metadata")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Complete extraction timestamp")


# Request/Response Models
class ExtractionRequest(BaseModel):
    """Request model for data extraction."""
    asteroid_name: str = Field(..., description="Name of asteroid to extract data for")
    impact_coordinates: Coordinate = Field(..., description="Impact location coordinates")
    include_regional_data: bool = Field(True, description="Whether to include regional data extraction")
    regional_radius_km: float = Field(100, gt=0, description="Radius for regional data extraction in km")


class ExtractionResponse(BaseModel):
    """Response model for data extraction."""
    success: bool = Field(..., description="Whether extraction was successful")
    data: Optional[ImpactData] = Field(None, description="Extracted impact data")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    warnings: List[str] = Field(default_factory=list, description="Any warnings encountered")
    extraction_time_seconds: float = Field(..., description="Total extraction time in seconds")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")


class ExtractionStatus(BaseModel):
    """Status model for extraction progress."""
    status: str = Field(..., description="Current extraction status")
    progress_percentage: float = Field(..., ge=0, le=100, description="Extraction progress percentage")
    current_step: str = Field(..., description="Current extraction step")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")

