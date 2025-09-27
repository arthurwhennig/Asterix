from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

from database.database import get_db
from database.models import Simulation, User, Asteroid
from api.routes.auth import get_current_user

router = APIRouter()

class SimulationCreate(BaseModel):
    asteroid_id: int
    name: str
    description: Optional[str] = None
    simulation_data: dict
    impact_data: Optional[dict] = None
    is_public: bool = False

class SimulationResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    simulation_data: dict
    impact_data: Optional[dict]
    is_public: bool
    created_at: datetime
    asteroid: dict

@router.post("/", response_model=SimulationResponse)
async def create_simulation(
    simulation: SimulationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new simulation"""
    # Check if asteroid exists
    asteroid = db.query(Asteroid).filter(Asteroid.id == simulation.asteroid_id).first()
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    
    db_simulation = Simulation(
        user_id=current_user.id,
        asteroid_id=simulation.asteroid_id,
        name=simulation.name,
        description=simulation.description,
        simulation_data=json.dumps(simulation.simulation_data),
        impact_data=json.dumps(simulation.impact_data) if simulation.impact_data else None,
        is_public=simulation.is_public
    )
    
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    
    # Return simulation with asteroid data
    return {
        "id": db_simulation.id,
        "name": db_simulation.name,
        "description": db_simulation.description,
        "simulation_data": json.loads(db_simulation.simulation_data),
        "impact_data": json.loads(db_simulation.impact_data) if db_simulation.impact_data else None,
        "is_public": db_simulation.is_public,
        "created_at": db_simulation.created_at,
        "asteroid": {
            "id": asteroid.id,
            "name": asteroid.name,
            "diameter": asteroid.diameter,
            "is_potentially_hazardous": asteroid.is_potentially_hazardous
        }
    }

@router.get("/", response_model=List[SimulationResponse])
async def get_simulations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    public_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get simulations (user's own or public ones)"""
    query = db.query(Simulation)
    
    if public_only:
        query = query.filter(Simulation.is_public == True)
    elif current_user:
        query = query.filter(
            (Simulation.user_id == current_user.id) | (Simulation.is_public == True)
        )
    else:
        query = query.filter(Simulation.is_public == True)
    
    simulations = query.order_by(Simulation.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for sim in simulations:
        asteroid = db.query(Asteroid).filter(Asteroid.id == sim.asteroid_id).first()
        result.append({
            "id": sim.id,
            "name": sim.name,
            "description": sim.description,
            "simulation_data": json.loads(sim.simulation_data),
            "impact_data": json.loads(sim.impact_data) if sim.impact_data else None,
            "is_public": sim.is_public,
            "created_at": sim.created_at,
            "asteroid": {
                "id": asteroid.id,
                "name": asteroid.name,
                "diameter": asteroid.diameter,
                "is_potentially_hazardous": asteroid.is_potentially_hazardous
            } if asteroid else None
        })
    
    return result

@router.get("/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(
    simulation_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Get a specific simulation"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    # Check if user can access this simulation
    if not simulation.is_public and (not current_user or simulation.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    asteroid = db.query(Asteroid).filter(Asteroid.id == simulation.asteroid_id).first()
    
    return {
        "id": simulation.id,
        "name": simulation.name,
        "description": simulation.description,
        "simulation_data": json.loads(simulation.simulation_data),
        "impact_data": json.loads(simulation.impact_data) if simulation.impact_data else None,
        "is_public": simulation.is_public,
        "created_at": simulation.created_at,
        "asteroid": {
            "id": asteroid.id,
            "name": asteroid.name,
            "diameter": asteroid.diameter,
            "is_potentially_hazardous": asteroid.is_potentially_hazardous
        } if asteroid else None
    }

@router.put("/{simulation_id}", response_model=SimulationResponse)
async def update_simulation(
    simulation_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a simulation"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if simulation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if name is not None:
        simulation.name = name
    if description is not None:
        simulation.description = description
    if is_public is not None:
        simulation.is_public = is_public
    
    db.commit()
    db.refresh(simulation)
    
    asteroid = db.query(Asteroid).filter(Asteroid.id == simulation.asteroid_id).first()
    
    return {
        "id": simulation.id,
        "name": simulation.name,
        "description": simulation.description,
        "simulation_data": json.loads(simulation.simulation_data),
        "impact_data": json.loads(simulation.impact_data) if simulation.impact_data else None,
        "is_public": simulation.is_public,
        "created_at": simulation.created_at,
        "asteroid": {
            "id": asteroid.id,
            "name": asteroid.name,
            "diameter": asteroid.diameter,
            "is_potentially_hazardous": asteroid.is_potentially_hazardous
        } if asteroid else None
    }

@router.delete("/{simulation_id}")
async def delete_simulation(
    simulation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a simulation"""
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    if simulation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db.delete(simulation)
    db.commit()
    
    return {"message": "Simulation deleted successfully"}
