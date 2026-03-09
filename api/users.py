from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_user, get_password_hash, get_current_admin_user, security
import uuid
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
    body: schemas.PointsUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Add points to a user (admin only) - points sent in request body"""
    try:
        db_user = db.query(models.User).filter(models.User.username == username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        updated_user = crud.update_user_points(db, db_user.id, body.points)
        return {"message": f"Added {body.points} points to user", "total_points": updated_user.total_points}
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

@router.patch("/{username}/admin-status", response_model=schemas.User)
async def update_admin_status(
    username: str,
    update: schemas.UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Toggle admin or active status for a user (admin only)"""
    if username == current_user.username:
        raise HTTPException(status_code=400, detail="You cannot change your own admin or active status")
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        updated_user = crud.update_item(db, db_user, update_data)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user status: {str(e)}")

@router.patch("/{username}/password")
async def set_user_password(
    username: str,
    body: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Set a new password for a user (admin only) - password sent in request body, never in URL"""
    if len(body.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db_user.hashed_password = get_password_hash(body.new_password)
        db.commit()
        return {"message": f"Password updated for user '{username}'"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update password: {str(e)}")

@router.post("/create", response_model=schemas.User)
async def create_user_admin(
    user_data: schemas.UserCreateAdmin,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new user or admin directly (admin only)"""
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    try:
        new_user = models.User(
            id=str(uuid.uuid4()),
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            is_active=True,
            is_admin=user_data.is_admin,
            total_points=0,
            today_points=0,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
