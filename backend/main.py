from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import redis
import os
from dotenv import load_dotenv

from database.database import get_db
from database.models import User, Asteroid, Game
from api.routes import auth, asteroids, games, simulations, data_extraction

load_dotenv()

app = FastAPI(
    title="Asterix API",
    description="API for asteroid visualization and simulation tool",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(asteroids.router, prefix="/api/asteroids", tags=["asteroids"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["simulations"])
app.include_router(data_extraction.router, tags=["data-extraction"])


@app.get("/")
async def root():
    return {"message": "Asterix API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
