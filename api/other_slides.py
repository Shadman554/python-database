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
from api.notifications import send_onesignal_notification
import uuid

# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_other_slides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    species: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all other slides with pagination and optional species filter"""
    try:
        query = db.query(models.OtherSlide)
        if species:
            query = query.filter(models.OtherSlide.species.ilike(f"%{species}%"))

        slides = query.order_by(models.OtherSlide.created_at.desc()).offset(skip).limit(limit).all()

        if species:
            total = query.count()
        else:
            total = crud.count_items(db, models.OtherSlide)

        return create_paginated_response(slides, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve other slides: {str(e)}")

@router.get("/{slide_name}", response_model=schemas.OtherSlide)
async def get_other_slide(slide_name: str, db: Session = Depends(get_db)):
    """Get a specific other slide by name"""
    db_slide = db.query(models.OtherSlide).filter(models.OtherSlide.name == slide_name).first()
    if not db_slide:
        raise HTTPException(status_code=404, detail="Other slide not found")
    return db_slide

@router.post("/", response_model=schemas.OtherSlide)
async def create_other_slide(
    slide: schemas.OtherSlideCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new other slide (admin only)"""
    try:
        slide_data = slide.dict()
        slide_data['id'] = str(uuid.uuid4())
        db_slide = crud.create_item(db, models.OtherSlide, slide_data)
        
        # Send notification for new other slide
        await send_onesignal_notification(
            title="New Slide Added",
            content=f"A new slide '{db_slide.name}' for {db_slide.species} has been added",
            custom_data={
                "slide_id": db_slide.id,
                "type": "other_slide",
                "species": db_slide.species
            }
        )
        
        return db_slide
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create other slide: {str(e)}")

@router.put("/{slide_name}", response_model=schemas.OtherSlide)
async def update_other_slide(
    slide_name: str,
    slide: schemas.OtherSlideCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update an other slide (admin only)"""
    db_slide = db.query(models.OtherSlide).filter(models.OtherSlide.name == slide_name).first()
    if not db_slide:
        raise HTTPException(status_code=404, detail="Other slide not found")

    try:
        updated_slide = crud.update_item(db, db_slide, slide.dict())
        return updated_slide
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update other slide: {str(e)}")

@router.delete("/{slide_name}")
async def delete_other_slide(
    slide_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete an other slide (admin only)"""
    db_slide = db.query(models.OtherSlide).filter(models.OtherSlide.name == slide_name).first()
    if not db_slide:
        raise HTTPException(status_code=404, detail="Other slide not found")

    try:
        crud.delete_item(db, db_slide)
        return {"message": "Other slide deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete other slide: {str(e)}")