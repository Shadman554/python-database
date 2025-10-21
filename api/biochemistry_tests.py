
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
from utils import create_paginated_response
import uuid

def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_biochemistry_tests(
    search: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all biochemistry tests with optional search and pagination"""
    try:
        query = db.query(models.BiochemistryTest)
        
        if search:
            query = query.filter(
                or_(
                    models.BiochemistryTest.name.ilike(f"%{search}%"),
                    models.BiochemistryTest.description.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        tests = query.order_by(models.BiochemistryTest.created_at.desc()).offset(offset).limit(limit).all()
        
        return create_paginated_response(tests, total, offset // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve biochemistry tests: {str(e)}")

@router.get("/by-name/{test_name}", response_model=schemas.BiochemistryTest)
async def get_biochemistry_test_by_name(test_name: str, db: Session = Depends(get_db)):
    """Get a specific biochemistry test by name"""
    test = db.query(models.BiochemistryTest).filter(models.BiochemistryTest.name == test_name).first()
    if not test:
        raise HTTPException(status_code=404, detail="Biochemistry test not found")
    return test

@router.post("/", response_model=schemas.BiochemistryTest, status_code=status.HTTP_201_CREATED)
async def create_biochemistry_test(
    test: schemas.BiochemistryTestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new biochemistry test (admin only)"""
    existing = db.query(models.BiochemistryTest).filter(models.BiochemistryTest.name == test.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Biochemistry test with this name already exists")
    
    try:
        test_data = test.dict()
        test_data['id'] = str(uuid.uuid4())
        db_test = crud.create_item(db, models.BiochemistryTest, test_data)
        
        # Send notification for new biochemistry test
        from utils import send_content_notification
        await send_content_notification("biochemistry_test", test_data.get('name', 'Unknown'), test_data['id'])
        
        return db_test
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create biochemistry test: {str(e)}")

@router.put("/{test_name}", response_model=schemas.BiochemistryTest)
async def update_biochemistry_test(
    test_name: str,
    test: schemas.BiochemistryTestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a biochemistry test (admin only)"""
    db_test = db.query(models.BiochemistryTest).filter(models.BiochemistryTest.name == test_name).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Biochemistry test not found")

    if test.name != test_name:
        existing = db.query(models.BiochemistryTest).filter(models.BiochemistryTest.name == test.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Biochemistry test with this name already exists")

    try:
        updated_test = crud.update_item(db, db_test, test.dict())
        return updated_test
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update biochemistry test: {str(e)}")

@router.delete("/{test_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_biochemistry_test(
    test_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a biochemistry test (admin only)"""
    db_test = db.query(models.BiochemistryTest).filter(models.BiochemistryTest.name == test_name).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Biochemistry test not found")

    try:
        crud.delete_item(db, db_test)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete biochemistry test: {str(e)}")
