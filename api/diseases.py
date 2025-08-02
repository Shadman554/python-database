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
async def get_diseases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get diseases with optional search and pagination"""
    try:
        if search:
            diseases = crud.search_diseases(db, search, skip, limit)
            total = crud.count_search_results(db, models.Disease, search)
        else:
            diseases = crud.get_items(db, models.Disease, skip, limit)
            total = crud.count_items(db, models.Disease)
        
        return create_paginated_response(diseases, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve diseases: {str(e)}")

@router.get("/by-name/{disease_name}", response_model=schemas.Disease)
async def get_disease_by_name(disease_name: str, db: Session = Depends(get_db)):
    """Get a specific disease by name"""
    disease = db.query(models.Disease).filter(models.Disease.name.ilike(f"%{disease_name}%")).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.get("/{disease_name}", response_model=schemas.Disease)
async def get_disease(disease_name: str, db: Session = Depends(get_db)):
    """Get a specific disease by name"""
    disease = db.query(models.Disease).filter(models.Disease.name == disease_name).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.post("/", response_model=schemas.Disease)
async def create_disease(
    disease: schemas.DiseaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new disease (admin only)"""
    try:
        disease_data = disease.dict()
        disease_data['id'] = str(uuid.uuid4())
        db_disease = crud.create_item(db, models.Disease, disease_data)
        
        # Send push notification for new disease
        from api.notifications import send_onesignal_notification
        await send_onesignal_notification(
            title="نەخۆشی نوێ",
            content=f"نەخۆشی نوێ زیادکراوە: {db_disease.name}",
            custom_data={
                "disease_id": db_disease.id,
                "type": "new_disease"
            }
        )
        
        return db_disease
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create disease: {str(e)}")

@router.put("/{disease_name}", response_model=schemas.Disease)
async def update_disease(
    disease_name: str,
    disease: schemas.DiseaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a disease (admin only)"""
    db_disease = db.query(models.Disease).filter(models.Disease.name == disease_name).first()
    if not db_disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    
    try:
        updated_disease = crud.update_item(db, db_disease, disease.dict())
        return updated_disease
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update disease: {str(e)}")

@router.delete("/{disease_name}")
async def delete_disease(
    disease_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a disease (admin only)"""
    db_disease = db.query(models.Disease).filter(models.Disease.name == disease_name).first()
    if not db_disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    
    try:
        crud.delete_item(db, db_disease)
        return {"message": "Disease deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete disease: {str(e)}")
