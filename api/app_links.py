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
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_app_links(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all app links with pagination"""
    try:
        links = crud.get_items(db, models.AppLink, skip, limit)
        total = crud.count_items(db, models.AppLink)
        return create_paginated_response(links, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve app links: {str(e)}")

@router.get("/{link_title}", response_model=schemas.AppLink)
async def get_app_link(link_title: str, db: Session = Depends(get_db)):
    """Get a specific app link by title"""
    link = db.query(models.AppLink).filter(models.AppLink.title == link_title).first()
    if not link:
        raise HTTPException(status_code=404, detail="App link not found")
    return link

@router.post("/", response_model=schemas.AppLink)
async def create_app_link(
    app_link: schemas.AppLinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new app link (admin only)"""
    try:
        link_data = app_link.dict()
        link_data['id'] = str(uuid.uuid4())
        db_link = crud.create_item(db, models.AppLink, link_data)
        return db_link
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create app link: {str(e)}")

@router.put("/{link_title}", response_model=schemas.AppLink)
async def update_app_link(
    link_title: str,
    app_link: schemas.AppLinkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update an app link (admin only)"""
    db_link = db.query(models.AppLink).filter(models.AppLink.title == link_title).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="App link not found")
    
    try:
        updated_link = crud.update_item(db, db_link, app_link.dict())
        return updated_link
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update app link: {str(e)}")

@router.delete("/{link_title}")
async def delete_app_link(
    link_title: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete an app link (admin only)"""
    db_link = db.query(models.AppLink).filter(models.AppLink.title == link_title).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="App link not found")
    
    try:
        crud.delete_item(db, db_link)
        return {"message": "App link deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete app link: {str(e)}")
