from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    game_scores = relationship("GameScore", back_populates=__tablename__)
    simulations = relationship("Simulation", back_populates=__tablename__)


class Asteroid(Base):
    __tablename__ = "asteroids"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    diameter = Column(Float)  # in meters
    mass = Column(Float)  # in kg
    velocity = Column(Float)  # in m/s
    distance_from_earth = Column(Float)  # in km
    is_potentially_hazardous = Column(Boolean, default=False)
    orbital_data = Column(Text)  # JSON string of orbital parameters
    nasa_id = Column(String, unique=True)  # NASA asteroid ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    simulations = relationship("Simulation", back_populates=__tablename__)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    level = Column(Integer, default=1)
    asteroids_destroyed = Column(Integer, default=0)
    time_survived = Column(Float)  # in seconds
    difficulty = Column(String, default="normal")  # easy, normal, hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates=__tablename__)


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asteroid_id = Column(Integer, ForeignKey("asteroids.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    simulation_data = Column(Text)  # JSON string of simulation parameters
    impact_data = Column(Text)  # JSON string of impact results
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates=__tablename__)
    asteroid = relationship("Asteroid", back_populates=__tablename__)


# Data Extraction Models
class ExtractionSession(Base):
    """Model for tracking data extraction sessions."""
    __tablename__ = "extraction_sessions"

    id = Column(Integer, primary_key=True, index=True)
    extraction_id = Column(String, unique=True, index=True, nullable=False)
    asteroid_name = Column(String, nullable=False)
    impact_latitude = Column(Float, nullable=False)
    impact_longitude = Column(Float, nullable=False)
    impact_altitude = Column(Float)
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    progress_percentage = Column(Float, default=0.0)
    current_step = Column(String)
    errors = Column(JSON)
    warnings = Column(JSON)
    data_sources = Column(JSON)
    extraction_time_seconds = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    extracted_asteroid_data = relationship("ExtractedAsteroidData", back_populates="extraction_session")
    extracted_topography_data = relationship("ExtractedTopographyData", back_populates="extraction_session")
    extracted_geological_data = relationship("ExtractedGeologicalData", back_populates="extraction_session")
    extracted_regional_data = relationship("ExtractedRegionalData", back_populates="extraction_session")


class ExtractedAsteroidData(Base):
    """Model for storing extracted asteroid data from NASA JPL."""
    __tablename__ = "extracted_asteroid_data"

    id = Column(Integer, primary_key=True, index=True)
    extraction_session_id = Column(Integer, ForeignKey("extraction_sessions.id"))
    name = Column(String, nullable=False)
    nasa_id = Column(String, nullable=False)
    diameter_m = Column(Float, nullable=False)
    velocity_ms = Column(Float, nullable=False)
    mass_kg = Column(Float)
    composition = Column(String)
    orbital_data = Column(JSON)
    close_approach_data = Column(JSON)
    is_potentially_hazardous = Column(Boolean, default=False)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    extraction_session = relationship("ExtractionSession", back_populates="extracted_asteroid_data")

    # Indexes
    __table_args__ = (
        Index('idx_asteroid_name', 'name'),
        Index('idx_nasa_id', 'nasa_id'),
        Index('idx_extraction_session', 'extraction_session_id'),
    )


class ExtractedTopographyData(Base):
    """Model for storing extracted topography data from NASA CMR."""
    __tablename__ = "extracted_topography_data"

    id = Column(Integer, primary_key=True, index=True)
    extraction_session_id = Column(Integer, ForeignKey("extraction_sessions.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    elevation_m = Column(Float, nullable=False)
    data_source = Column(String, nullable=False)
    resolution_m = Column(Float)
    confidence_level = Column(Float)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    extraction_session = relationship("ExtractionSession", back_populates="extracted_topography_data")

    # Indexes
    __table_args__ = (
        Index('idx_coordinates', 'latitude', 'longitude'),
        Index('idx_extraction_session', 'extraction_session_id'),
    )


class ExtractedGeologicalData(Base):
    """Model for storing extracted geological data from OneGeology."""
    __tablename__ = "extracted_geological_data"

    id = Column(Integer, primary_key=True, index=True)
    extraction_session_id = Column(Integer, ForeignKey("extraction_sessions.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    geological_description = Column(Text, nullable=False)
    material_type = Column(String)
    density_kg_m3 = Column(Float, nullable=False)
    age_period = Column(String)
    formation_name = Column(String)
    data_source = Column(String, nullable=False)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    extraction_session = relationship("ExtractionSession", back_populates="extracted_geological_data")

    # Indexes
    __table_args__ = (
        Index('idx_coordinates', 'latitude', 'longitude'),
        Index('idx_material_type', 'material_type'),
        Index('idx_extraction_session', 'extraction_session_id'),
    )


class ExtractedRegionalData(Base):
    """Model for storing extracted regional data."""
    __tablename__ = "extracted_regional_data"

    id = Column(Integer, primary_key=True, index=True)
    extraction_session_id = Column(Integer, ForeignKey("extraction_sessions.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    
    # Fault data
    fault_name = Column(String)
    fault_distance_km = Column(Float)
    fault_type = Column(String)
    fault_activity_status = Column(String)
    fault_slip_rate = Column(Float)
    
    # Bathymetry data
    depth_m = Column(Float)
    is_land = Column(Boolean, default=True)
    
    # Population data
    total_population = Column(Integer)
    population_density_km2 = Column(Float)
    affected_area_km2 = Column(Float)
    major_cities = Column(JSON)
    
    # Infrastructure data
    airports = Column(JSON)
    ports = Column(JSON)
    power_plants = Column(JSON)
    hospitals = Column(JSON)
    schools = Column(JSON)
    
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    extraction_session = relationship("ExtractionSession", back_populates="extracted_regional_data")

    # Indexes
    __table_args__ = (
        Index('idx_coordinates', 'latitude', 'longitude'),
        Index('idx_extraction_session', 'extraction_session_id'),
    )


class ImpactCalculation(Base):
    """Model for storing calculated impact parameters."""
    __tablename__ = "impact_calculations"

    id = Column(Integer, primary_key=True, index=True)
    extraction_session_id = Column(Integer, ForeignKey("extraction_sessions.id"))
    
    # Impact parameters
    impact_energy_joules = Column(Float, nullable=False)
    impact_energy_megatons = Column(Float, nullable=False)
    crater_diameter_km = Column(Float, nullable=False)
    crater_depth_km = Column(Float, nullable=False)
    
    # Additional calculated parameters
    fireball_radius_km = Column(Float)
    thermal_radiation_radius_km = Column(Float)
    blast_wave_radius_km = Column(Float)
    richter_magnitude = Column(Float)
    tsunami_wave_height_meters = Column(Float)
    
    # Calculation metadata
    calculation_method = Column(String, default="simplified_scaling_laws")
    calculation_version = Column(String, default="1.0")
    calculation_metadata = Column(JSON)
    
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    extraction_session = relationship("ExtractionSession")

    # Indexes
    __table_args__ = (
        Index('idx_extraction_session', 'extraction_session_id'),
        Index('idx_impact_energy', 'impact_energy_joules'),
    )
