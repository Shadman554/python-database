from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
# Dependency function for admin authentication
def get_admin_user(db: Session = Depends(get_db)):
    return get_current_admin_user(security, db)

from utils import create_paginated_response
import uuid

router = APIRouter()

@router.get("/by-name/{staff_name}", response_model=schemas.Staff)
async def get_staff_by_name(staff_name: str, db: Session = Depends(get_db)):
    """Get a specific staff member by name"""
    staff = db.query(models.Staff).filter(models.Staff.name.ilike(f"%{staff_name}%")).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_staff(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all staff members with pagination"""
    try:
        staff = crud.get_items(db, models.Staff, skip, limit)
        total = crud.count_items(db, models.Staff)
        return create_paginated_response(staff, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve staff: {str(e)}")

@router.get("/{staff_name}", response_model=schemas.Staff)
async def get_staff_member(staff_name: str, db: Session = Depends(get_db)):
    """Get a specific staff member by name"""
    staff = db.query(models.Staff).filter(models.Staff.name == staff_name).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.post("/", response_model=schemas.Staff)
async def create_staff(
    staff: schemas.StaffCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new staff member (admin only)"""
    try:
        staff_data = staff.dict()
        staff_data['id'] = str(uuid.uuid4())
        db_staff = crud.create_item(db, models.Staff, staff_data)
        return db_staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create staff member: {str(e)}")

@router.put("/{staff_name}", response_model=schemas.Staff)
async def update_staff(
    staff_name: str,
    staff: schemas.StaffCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a staff member (admin only)"""
    db_staff = db.query(models.Staff).filter(models.Staff.name == staff_name).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    try:
        updated_staff = crud.update_item(db, db_staff, staff.dict())
        return updated_staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update staff member: {str(e)}")

@router.delete("/{staff_name}")
async def delete_staff(
    staff_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a staff member (admin only)"""
    db_staff = db.query(models.Staff).filter(models.Staff.name == staff_name).first()
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    try:
        crud.delete_item(db, db_staff)
        return {"message": "Staff member deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete staff member: {str(e)}")
