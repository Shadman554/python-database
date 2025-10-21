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
async def get_drugs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    drug_class: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get drugs with optional filtering and pagination"""
    try:
        if search:
            drugs = crud.search_drugs(db, search, skip, limit)
            total = crud.count_search_results(db, models.Drug, search)
        elif drug_class:
            drugs = crud.filter_drugs_by_class(db, drug_class, skip, limit)
            total = db.query(models.Drug).filter(models.Drug.drug_class == drug_class).count()
        else:
            drugs = crud.get_items(db, models.Drug, skip, limit)
            total = crud.count_items(db, models.Drug)
        
        return create_paginated_response(drugs, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve drugs: {str(e)}")

@router.get("/by-name/{drug_name}", response_model=schemas.Drug)
async def get_drug_by_name(drug_name: str, db: Session = Depends(get_db)):
    """Get a specific drug by name"""
    drug = db.query(models.Drug).filter(models.Drug.name.ilike(f"%{drug_name}%")).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug

@router.get("/{drug_name}", response_model=schemas.Drug)
async def get_drug(drug_name: str, db: Session = Depends(get_db)):
    """Get a specific drug by name"""
    drug = db.query(models.Drug).filter(models.Drug.name == drug_name).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug

@router.post("/", response_model=schemas.Drug)
async def create_drug(
    drug: schemas.DrugCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new drug (admin only)"""
    try:
        drug_data = drug.dict()
        drug_data['id'] = str(uuid.uuid4())
        db_drug = crud.create_item(db, models.Drug, drug_data)
        
        # Send notification for new drug
        from utils import send_content_notification
        await send_content_notification("drug", drug_data.get('name', 'Unknown'), drug_data['id'])
        
        return db_drug
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create drug: {str(e)}")

@router.put("/{drug_name}", response_model=schemas.Drug)
async def update_drug(
    drug_name: str,
    drug: schemas.DrugCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a drug (admin only)"""
    db_drug = db.query(models.Drug).filter(models.Drug.name == drug_name).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    try:
        updated_drug = crud.update_item(db, db_drug, drug.dict())
        return updated_drug
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update drug: {str(e)}")

@router.delete("/{drug_name}")
async def delete_drug(
    drug_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a drug (admin only)"""
    db_drug = db.query(models.Drug).filter(models.Drug.name == drug_name).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    try:
        crud.delete_item(db, db_drug)
        return {"message": "Drug deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete drug: {str(e)}")

@router.get("/classes/list")
async def get_drug_classes(db: Session = Depends(get_db)):
    """Get all unique drug classes"""
    try:
        classes = db.query(models.Drug.drug_class).distinct().all()
        return {"classes": [cls[0] for cls in classes if cls[0]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get drug classes: {str(e)}")
