from fastapi import APIRouter, Depe\nfrom fastapi.security import HTTPAuthorizationCredentialsnds, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
from utils import create_paginated_response
import uuid
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all notifications with pagination"""
    try:
        notifications = db.query(models.Notification).order_by(models.Notification.timestamp.desc()).offset(skip).limit(limit).all()
        total = crud.count_items(db, models.Notification)
        return create_paginated_response(notifications, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notifications: {str(e)}")

@router.get("/{notification_title}", response_model=schemas.Notification)
async def get_notification(notification_title: str, db: Session = Depends(get_db)):
    """Get a specific notification by title"""
    notification = db.query(models.Notification).filter(models.Notification.title == notification_title).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/", response_model=schemas.Notification)
async def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new notification (admin only)"""
    try:
        notification_data = notification.dict()
        notification_data['id'] = str(uuid.uuid4())
        db_notification = crud.create_item(db, models.Notification, notification_data)
        return db_notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notification: {str(e)}")

@router.put("/{notification_title}", response_model=schemas.Notification)
async def update_notification(
    notification_title: str,
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a notification (admin only)"""
    db_notification = db.query(models.Notification).filter(models.Notification.title == notification_title).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    try:
        updated_notification = crud.update_item(db, db_notification, notification.dict())
        return updated_notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update notification: {str(e)}")

@router.delete("/{notification_title}")
async def delete_notification(
    notification_title: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a notification (admin only)"""
    db_notification = db.query(models.Notification).filter(models.Notification.title == notification_title).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    try:
        crud.delete_item(db, db_notification)
        return {"message": "Notification deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete notification: {str(e)}")

@router.get("/recent/latest")
async def get_recent_notifications(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get recent notifications"""
    try:
        notifications = db.query(models.Notification).order_by(models.Notification.timestamp.desc()).limit(limit).all()
        return {"notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recent notifications: {str(e)}")
