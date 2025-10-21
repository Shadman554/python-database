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

async def send_onesignal_notification(title: str, content: str, custom_data: dict = None):
    """Send push notification via OneSignal"""
    try:
        onesignal_app_id = os.getenv("ONESIGNAL_APP_ID")
        onesignal_rest_api_key = os.getenv("ONESIGNAL_REST_API_KEY")
        
        if not onesignal_app_id or not onesignal_rest_api_key:
            print("OneSignal credentials not configured")
            return False
        
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Authorization": f"Basic {onesignal_rest_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "app_id": onesignal_app_id,
            "included_segments": ["All"],
            "headings": {"en": title},
            "contents": {"en": content}
        }
        
        if custom_data:
            payload["data"] = custom_data
        
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 200
            
    except Exception as e:
        print(f"Error sending OneSignal notification: {str(e)}")
        return False
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_urine_slides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    species: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all urine slides with pagination and optional species filter"""
    try:
        query = db.query(models.UrineSlide)
        if species:
            query = query.filter(models.UrineSlide.species.ilike(f"%{species}%"))

        slides = query.order_by(models.UrineSlide.created_at.desc()).offset(skip).limit(limit).all()

        if species:
            total = query.count()
        else:
            total = crud.count_items(db, models.UrineSlide)

        return create_paginated_response(slides, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve urine slides: {str(e)}")

@router.get("/{slide_name}", response_model=schemas.UrineSlide)
async def read_urine_slide(slide_name: str, db: Session = Depends(get_db)):
    """Get a specific urine slide by name"""
    db_slide = db.query(models.UrineSlide).filter(models.UrineSlide.name == slide_name).first()
    if db_slide is None:
        raise HTTPException(status_code=404, detail="Urine slide not found")
    return db_slide

@router.post("/", response_model=schemas.UrineSlide)
async def create_urine_slide(
    slide: schemas.UrineSlideCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new urine slide (admin only)"""
    try:
        slide_data = slide.dict()
        slide_data['id'] = str(uuid.uuid4())
        db_slide = crud.create_item(db, models.UrineSlide, slide_data)
        
        # Send notification for new urine slide
        await send_onesignal_notification(
            title="New Urine Slide Added",
            content=f"A new urine slide '{db_slide.name}' for {db_slide.species} has been added",
            custom_data={
                "slide_id": db_slide.id,
                "type": "urine_slide",
                "species": db_slide.species
            }
        )
        
        return db_slide
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create urine slide: {str(e)}")

@router.put("/{slide_name}", response_model=schemas.UrineSlide)
async def update_urine_slide(
    slide_name: str,
    slide: schemas.UrineSlideCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a urine slide (admin only)"""
    db_slide = db.query(models.UrineSlide).filter(models.UrineSlide.name == slide_name).first()
    if not db_slide:
        raise HTTPException(status_code=404, detail="Urine slide not found")

    try:
        updated_slide = crud.update_item(db, db_slide, slide.dict())
        return updated_slide
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update urine slide: {str(e)}")

@router.delete("/{slide_name}")
async def delete_urine_slide(
    slide_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a urine slide (admin only)"""
    db_slide = db.query(models.UrineSlide).filter(models.UrineSlide.name == slide_name).first()
    if not db_slide:
        raise HTTPException(status_code=404, detail="Urine slide not found")

    try:
        crud.delete_item(db, db_slide)
        return {"message": "Urine slide deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete urine slide: {str(e)}")