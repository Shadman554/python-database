
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter()

@router.get("/")
async def get_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get leaderboard of users ordered by total points"""
    try:
        users = db.query(models.User).order_by(models.User.total_points.desc()).limit(limit).all()
        return {
            "leaderboard": [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "total_points": user.total_points
                }
                for i, user in enumerate(users)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")
