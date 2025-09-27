from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from database.models import Game, User
from api.routes.auth import get_current_user

router = APIRouter()


class GameCreate(BaseModel):
    score: int
    level: int = 1
    asteroids_destroyed: int = 0
    time_survived: float
    difficulty: str = "normal"


class GameResponse(BaseModel):
    id: int
    score: int
    level: int
    asteroids_destroyed: int
    time_survived: float
    difficulty: str
    created_at: datetime


@router.post("/score", response_model=GameResponse)
async def submit_score(
    score_data: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a game score"""
    game = Game(
        user_id=current_user.id,
        score=score_data.score,
        level=score_data.level,
        asteroids_destroyed=score_data.asteroids_destroyed,
        time_survived=score_data.time_survived,
        difficulty=score_data.difficulty,
    )

    db.add(game)
    db.commit()
    db.refresh(game)

    return game


@router.get("/scores", response_model=List[GameResponse])
async def get_user_scores(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user's game scores"""
    query = db.query(Game).filter(Game.user_id == current_user.id)

    if difficulty:
        query = query.filter(Game.difficulty == difficulty)

    scores = query.order_by(Game.score.desc()).offset(skip).limit(limit).all()
    return scores


@router.get("/leaderboard", response_model=List[GameResponse])
async def get_leaderboard(
    difficulty: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get global leaderboard"""
    query = db.query(Game)

    if difficulty:
        query = query.filter(Game.difficulty == difficulty)

    scores = query.order_by(Game.score.desc()).limit(limit).all()
    return scores


@router.get("/stats")
async def get_user_stats(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get user's game statistics"""
    scores = db.query(Game).filter(Game.user_id == current_user.id).all()

    if not scores:
        return {
            "total_games": 0,
            "high_score": 0,
            "total_asteroids_destroyed": 0,
            "total_time_survived": 0,
            "average_score": 0,
        }

    total_games = len(scores)
    high_score = max(score.score for score in scores)
    total_asteroids_destroyed = sum(score.asteroids_destroyed for score in scores)
    total_time_survived = sum(score.time_survived for score in scores)
    average_score = sum(score.score for score in scores) / total_games

    return {
        "total_games": total_games,
        "high_score": high_score,
        "total_asteroids_destroyed": total_asteroids_destroyed,
        "total_time_survived": total_time_survived,
        "average_score": round(average_score, 2),
    }
