
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user

router = APIRouter()
security = HTTPBearer(auto_error=False)

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


@router.get("/my-rank")
async def get_my_rank(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get the current user's rank, points, and total player count from the full leaderboard"""
    try:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Authentication required")

        current_user = get_current_user(credentials, db)
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        # Get all non-admin users ordered by points to calculate true rank
        all_users = db.query(models.User).filter(
            models.User.is_admin != True
        ).order_by(models.User.total_points.desc()).all()

        user_rank = 0
        total_players = len(all_users)

        for i, u in enumerate(all_users):
            if u.id == current_user.id:
                user_rank = i + 1
                break

        return {
            "rank": user_rank,
            "total_points": current_user.total_points,
            "today_points": current_user.today_points,
            "total_players": total_players,
            "username": current_user.username,
            "photo_url": current_user.photo_url,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user rank: {str(e)}")
