
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
async def get_other_tests(
    search: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all other tests with optional search and pagination"""
    try:
        query = db.query(models.OtherTest)
        
        if search:
            query = query.filter(
                or_(
                    models.OtherTest.name.ilike(f"%{search}%"),
                    models.OtherTest.description.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        tests = query.order_by(models.OtherTest.created_at.desc()).offset(offset).limit(limit).all()
        
        return create_paginated_response(tests, total, offset // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve other tests: {str(e)}")

@router.get("/by-name/{test_name}", response_model=schemas.OtherTestModel)
async def get_other_test_by_name(test_name: str, db: Session = Depends(get_db)):
    """Get a specific other test by name"""
    test = db.query(models.OtherTest).filter(models.OtherTest.name == test_name).first()
    if not test:
        raise HTTPException(status_code=404, detail="Other test not found")
    return test

@router.post("/", response_model=schemas.OtherTestModel, status_code=status.HTTP_201_CREATED)
async def create_other_test(
    test: schemas.OtherTestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new other test (admin only)"""
    existing = db.query(models.OtherTest).filter(models.OtherTest.name == test.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Other test with this name already exists")
    
    try:
        test_data = test.dict()
        test_data['id'] = str(uuid.uuid4())
        db_test = crud.create_item(db, models.OtherTest, test_data)
        
        # Send notification for new other test
        from utils import send_content_notification
        await send_content_notification("other_test", test_data.get('name', 'Unknown'), test_data['id'])
        
        return db_test
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create other test: {str(e)}")

@router.put("/{test_name}", response_model=schemas.OtherTestModel)
async def update_other_test(
    test_name: str,
    test: schemas.OtherTestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update an other test (admin only)"""
    db_test = db.query(models.OtherTest).filter(models.OtherTest.name == test_name).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Other test not found")

    if test.name != test_name:
        existing = db.query(models.OtherTest).filter(models.OtherTest.name == test.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Other test with this name already exists")

    try:
        updated_test = crud.update_item(db, db_test, test.dict())
        return updated_test
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update other test: {str(e)}")

@router.delete("/{test_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_other_test(
    test_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete an other test (admin only)"""
    db_test = db.query(models.OtherTest).filter(models.OtherTest.name == test_name).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Other test not found")

    try:
        crud.delete_item(db, db_test)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete other test: {str(e)}")
