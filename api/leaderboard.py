
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
    """Get leaderboard of users ordered by total points (excludes admin accounts)"""
    try:
        # Filter out admin accounts from leaderboard
        users = db.query(models.User).filter(
            models.User.is_admin != True
        ).order_by(models.User.total_points.desc()).limit(limit).all()
        
        return {
            "leaderboard": [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "total_points": user.total_points,
                    "photo_url": user.photo_url,
                    "is_admin": user.is_admin if hasattr(user, 'is_admin') else False
                }
                for i, user in enumerate(users)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")
