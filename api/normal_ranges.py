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

@router.get("/by-name/{range_name}", response_model=schemas.NormalRange)
async def get_range_by_name(range_name: str, db: Session = Depends(get_db)):
    """Get a specific normal range by name"""
    range_data = db.query(models.NormalRange).filter(models.NormalRange.name.ilike(f"%{range_name}%")).first()
    if not range_data:
        raise HTTPException(status_code=404, detail="Normal range not found")
    return range_data

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_normal_ranges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    species: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get normal ranges with optional filtering and pagination"""
    try:
        if species:
            ranges = crud.filter_normal_ranges_by_species(db, species, skip, limit)
            total = db.query(models.NormalRange).filter(models.NormalRange.species == species).count()
        elif category:
            ranges = crud.filter_normal_ranges_by_category(db, category, skip, limit)
            total = db.query(models.NormalRange).filter(models.NormalRange.category == category).count()
        else:
            ranges = crud.get_items(db, models.NormalRange, skip, limit)
            total = crud.count_items(db, models.NormalRange)
        
        return create_paginated_response(ranges, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve normal ranges: {str(e)}")

@router.get("/{range_name}", response_model=schemas.NormalRange)
async def get_normal_range(range_name: str, db: Session = Depends(get_db)):
    """Get a specific normal range by name"""
    range_item = db.query(models.NormalRange).filter(models.NormalRange.name == range_name).first()
    if not range_item:
        raise HTTPException(status_code=404, detail="Normal range not found")
    return range_item

@router.post("/", response_model=schemas.NormalRange)
async def create_normal_range(
    normal_range: schemas.NormalRangeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new normal range (admin only)"""
    try:
        range_data = normal_range.dict()
        range_data['id'] = str(uuid.uuid4())
        db_range = crud.create_item(db, models.NormalRange, range_data)
        return db_range
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create normal range: {str(e)}")

@router.put("/{range_name}", response_model=schemas.NormalRange)
async def update_normal_range(
    range_name: str,
    normal_range: schemas.NormalRangeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a normal range (admin only)"""
    db_range = db.query(models.NormalRange).filter(models.NormalRange.name == range_name).first()
    if not db_range:
        raise HTTPException(status_code=404, detail="Normal range not found")
    
    try:
        updated_range = crud.update_item(db, db_range, normal_range.dict())
        return updated_range
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update normal range: {str(e)}")

@router.delete("/{range_name}")
async def delete_normal_range(
    range_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a normal range (admin only)"""
    db_range = db.query(models.NormalRange).filter(models.NormalRange.name == range_name).first()
    if not db_range:
        raise HTTPException(status_code=404, detail="Normal range not found")
    
    try:
        crud.delete_item(db, db_range)
        return {"message": "Normal range deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete normal range: {str(e)}")

@router.get("/species/list")
async def get_species_list(db: Session = Depends(get_db)):
    """Get all unique species"""
    try:
        species = db.query(models.NormalRange.species).distinct().all()
        return {"species": [sp[0] for sp in species if sp[0]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get species list: {str(e)}")

@router.get("/categories/list")
async def get_categories_list(db: Session = Depends(get_db)):
    """Get all unique categories"""
    try:
        categories = db.query(models.NormalRange.category).distinct().all()
        return {"categories": [cat[0] for cat in categories if cat[0]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories list: {str(e)}")
