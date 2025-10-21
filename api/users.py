from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_user, get_password_hash, get_current_admin_user, security
from utils import create_paginated_response
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    current_user = get_current_user(credentials, db)
    return current_user

@router.delete("/me")
async def delete_my_account(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete current user's own account"""
    try:
        current_user = get_current_user(credentials, db)
        
        # Delete the user's account
        crud.delete_item(db, current_user)
        
        return {"message": "Account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Get all users (admin only)"""
    try:
        users = crud.get_items(db, models.User, skip, limit)
        total = crud.count_items(db, models.User)
        return create_paginated_response(users, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")

@router.get("/{username}", response_model=schemas.User)
async def get_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Get a specific user by username (admin only)"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{username}", response_model=schemas.User)
async def update_user(
    username: str,
    user_update: schemas.UserBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a user (admin only)"""
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        updated_user = crud.update_item(db, db_user, user_update.dict())
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

@router.delete("/{username}")
async def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a user (admin only)"""
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        crud.delete_item(db, db_user)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

@router.post("/{username}/points")
async def add_user_points(
    username: str,
    points: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Add points to a user (admin only)"""
    try:
        db_user = db.query(models.User).filter(models.User.username == username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user = crud.update_user_points(db, db_user.id, points)
        return {"message": f"Added {points} points to user", "total_points": updated_user.total_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add points: {str(e)}")

@router.get("/leaderboard/top")
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get top users by points"""
    try:
        users = db.query(models.User).order_by(models.User.total_points.desc()).limit(limit).all()
        return {
            "leaderboard": [
                {
                    "rank": i + 1,
                    "username": user.username,
                    "total_points": user.total_points,
                    "today_points": user.today_points
                }
                for i, user in enumerate(users)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get leaderboard: {str(e)}")

@router.post("/reset-daily-points")
async def reset_daily_points(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Reset daily points for all users (admin only)"""
    try:
        db.query(models.User).update({models.User.today_points: 0})
        db.commit()
        return {"message": "Daily points reset for all users"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset daily points: {str(e)}")
