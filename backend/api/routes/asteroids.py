from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import requests
import os
from dotenv import load_dotenv

from database.database import get_db
from database.models import Asteroid, User
from api.routes.auth import get_current_user

load_dotenv()

router = APIRouter()

NASA_API_KEY = os.getenv("NASA_API_KEY", "")

class AsteroidResponse(BaseModel):
    id: int
    name: str
    diameter: Optional[float]
    mass: Optional[float]
    velocity: Optional[float]
    distance_from_earth: Optional[float]
    is_potentially_hazardous: bool
    nasa_id: Optional[str]

@router.get("/", response_model=List[AsteroidResponse])
async def get_asteroids(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    hazardous_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Asteroid)
    
    if hazardous_only:
        query = query.filter(Asteroid.is_potentially_hazardous == True)
    
    asteroids = query.offset(skip).limit(limit).all()
    return asteroids

@router.get("/{asteroid_id}", response_model=AsteroidResponse)
async def get_asteroid(asteroid_id: int, db: Session = Depends(get_db)):
    asteroid = db.query(Asteroid).filter(Asteroid.id == asteroid_id).first()
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    return asteroid

@router.post("/sync-nasa")
async def sync_nasa_data(db: Session = Depends(get_db)):
    """Sync asteroid data from NASA API"""
    if not NASA_API_KEY:
        raise HTTPException(status_code=400, detail="NASA API key not configured")
    
    try:
        # Fetch data from NASA NEO API
        url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={NASA_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        near_earth_objects = data.get("near_earth_objects", {})
        
        synced_count = 0
        for date, asteroids in near_earth_objects.items():
            for asteroid_data in asteroids:
                nasa_id = asteroid_data.get("id")
                
                # Check if asteroid already exists
                existing = db.query(Asteroid).filter(Asteroid.nasa_id == nasa_id).first()
                if existing:
                    continue
                
                # Extract asteroid information
                name = asteroid_data.get("name", "Unknown")
                diameter = None
                if "estimated_diameter" in asteroid_data:
                    meters = asteroid_data["estimated_diameter"].get("meters", {})
                    if meters:
                        diameter = (meters.get("estimated_diameter_min", 0) + meters.get("estimated_diameter_max", 0)) / 2
                
                # Calculate velocity (simplified)
                velocity = None
                if "close_approach_data" in asteroid_data and asteroid_data["close_approach_data"]:
                    close_approach = asteroid_data["close_approach_data"][0]
                    relative_velocity = close_approach.get("relative_velocity", {})
                    if "kilometers_per_second" in relative_velocity:
                        velocity = float(relative_velocity["kilometers_per_second"]) * 1000  # Convert to m/s
                
                # Get distance from Earth
                distance_from_earth = None
                if "close_approach_data" in asteroid_data and asteroid_data["close_approach_data"]:
                    close_approach = asteroid_data["close_approach_data"][0]
                    miss_distance = close_approach.get("miss_distance", {})
                    if "kilometers" in miss_distance:
                        distance_from_earth = float(miss_distance["kilometers"])
                
                is_hazardous = asteroid_data.get("is_potentially_hazardous_asteroid", False)
                
                # Create asteroid record
                asteroid = Asteroid(
                    name=name,
                    diameter=diameter,
                    velocity=velocity,
                    distance_from_earth=distance_from_earth,
                    is_potentially_hazardous=is_hazardous,
                    nasa_id=nasa_id,
                    orbital_data=str(asteroid_data.get("orbital_data", {}))
                )
                
                db.add(asteroid)
                synced_count += 1
        
        db.commit()
        return {"message": f"Successfully synced {synced_count} asteroids from NASA API"}
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from NASA API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing data: {str(e)}")

@router.post("/", response_model=AsteroidResponse)
async def create_asteroid(
    name: str,
    diameter: Optional[float] = None,
    mass: Optional[float] = None,
    velocity: Optional[float] = None,
    distance_from_earth: Optional[float] = None,
    is_potentially_hazardous: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a fictional asteroid"""
    asteroid = Asteroid(
        name=name,
        diameter=diameter,
        mass=mass,
        velocity=velocity,
        distance_from_earth=distance_from_earth,
        is_potentially_hazardous=is_potentially_hazardous
    )
    
    db.add(asteroid)
    db.commit()
    db.refresh(asteroid)
    
    return asteroid
