from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
from utils import create_paginated_response
import uuid

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_tutorial_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all tutorial videos with pagination"""
    try:
        videos = db.query(models.TutorialVideo).order_by(models.TutorialVideo.created_at.desc()).offset(skip).limit(limit).all()
        total = crud.count_items(db, models.TutorialVideo)
        return create_paginated_response(videos, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tutorial videos: {str(e)}")

@router.get("/{video_id}", response_model=schemas.TutorialVideo)
async def get_tutorial_video(video_id: str, db: Session = Depends(get_db)):
    """Get a specific tutorial video by ID"""
    video = crud.get_item(db, models.TutorialVideo, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Tutorial video not found")
    return video

@router.post("/", response_model=schemas.TutorialVideo)
async def create_tutorial_video(
    video: schemas.TutorialVideoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Create a new tutorial video (admin only)"""
    try:
        video_data = video.dict()
        video_data['id'] = str(uuid.uuid4())
        db_video = crud.create_item(db, models.TutorialVideo, video_data)
        return db_video
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tutorial video: {str(e)}")

@router.put("/{video_id}", response_model=schemas.TutorialVideo)
async def update_tutorial_video(
    video_id: str,
    video: schemas.TutorialVideoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Update a tutorial video (admin only)"""
    db_video = crud.get_item(db, models.TutorialVideo, video_id)
    if not db_video:
        raise HTTPException(status_code=404, detail="Tutorial video not found")
    
    try:
        updated_video = crud.update_item(db, db_video, video.dict())
        return updated_video
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update tutorial video: {str(e)}")

@router.delete("/{video_id}")
async def delete_tutorial_video(
    video_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Delete a tutorial video (admin only)"""
    db_video = crud.get_item(db, models.TutorialVideo, video_id)
    if not db_video:
        raise HTTPException(status_code=404, detail="Tutorial video not found")
    
    try:
        crud.delete_item(db, db_video)
        return {"message": "Tutorial video deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete tutorial video: {str(e)}")
