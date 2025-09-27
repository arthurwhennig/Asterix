from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
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
