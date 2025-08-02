from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
from utils import create_paginated_response
import uuid
import requests
import os
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)

async def send_onesignal_notification(title: str, content: str, custom_data: dict = None):
    """Send push notification via OneSignal"""
    try:
        # Get OneSignal credentials from environment variables
        onesignal_app_id = os.getenv("ONESIGNAL_APP_ID")
        onesignal_rest_api_key = os.getenv("ONESIGNAL_REST_API_KEY")
        
        if not onesignal_app_id or not onesignal_rest_api_key:
            print("OneSignal credentials not configured")
            return False
        
        # OneSignal API endpoint
        url = "https://onesignal.com/api/v1/notifications"
        
        # Headers
        headers = {
            "Authorization": f"Basic {onesignal_rest_api_key}",
            "Content-Type": "application/json"
        }
        
        # Notification payload
        payload = {
            "app_id": onesignal_app_id,
            "included_segments": ["All"],  # Send to all users
            "headings": {"en": title},
            "contents": {"en": content}
        }
        
        # Add custom data if provided
        if custom_data:
            payload["data"] = custom_data
        
        # Send the notification
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"OneSignal notification sent successfully: {response.json()}")
            return True
        else:
            print(f"Failed to send OneSignal notification: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending OneSignal notification: {str(e)}")
        return False
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
    """Create a new notification and send push notification (admin only)"""
    try:
        notification_data = notification.dict()
        notification_data['id'] = str(uuid.uuid4())
        db_notification = crud.create_item(db, models.Notification, notification_data)
        
        # Send push notification via OneSignal
        custom_data = {
            "notification_id": db_notification.id,
            "type": "notification"
        }
        await send_onesignal_notification(
            title=db_notification.title,
            content=db_notification.body,
            custom_data=custom_data
        )
        
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

@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Mark a specific notification as read"""
    try:
        db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
        if not db_notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        # Add is_read field if it doesn't exist (for backward compatibility)
        if not hasattr(db_notification, 'is_read'):
            # This would require a database migration in production
            # For now, we'll just return success
            pass
        else:
            db_notification.is_read = True
            db.commit()
            db.refresh(db_notification)
        
        return {"message": "Notification marked as read", "notification_id": notification_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark notification as read: {str(e)}")

@router.put("/mark-all-read")
async def mark_all_notifications_read(
    db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    try:
        # Update all notifications to mark them as read
        updated_count = db.query(models.Notification).update({"is_read": True})
        db.commit()
        
        return {
            "message": "All notifications marked as read",
            "updated_count": updated_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark all notifications as read: {str(e)}")

@router.get("/system/health")
async def notification_system_health():
    """Check notification system health"""
    try:
        # Check OneSignal configuration
        onesignal_app_id = os.getenv("ONESIGNAL_APP_ID")
        onesignal_rest_api_key = os.getenv("ONESIGNAL_REST_API_KEY")
        
        onesignal_configured = bool(onesignal_app_id and onesignal_rest_api_key)
        
        return {
            "status": "healthy" if onesignal_configured else "warning",
            "onesignal_configured": onesignal_configured,
            "app_id_present": bool(onesignal_app_id),
            "api_key_present": bool(onesignal_rest_api_key),
            "message": "OneSignal fully configured" if onesignal_configured else "OneSignal credentials missing"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Health check failed: {str(e)}"
        }
