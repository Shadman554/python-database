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
async def get_instruments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all instruments with pagination"""
    try:
        instruments = db.query(models.Instrument).order_by(models.Instrument.created_at.desc()).offset(skip).limit(limit).all()
        total = crud.count_items(db, models.Instrument)
        return create_paginated_response(instruments, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve instruments: {str(e)}")

@router.get("/{instrument_name}", response_model=schemas.Instrument)
async def read_instrument(instrument_name: str, db: Session = Depends(get_db)):
    """Get a specific instrument by name"""
    db_instrument = db.query(models.Instrument).filter(models.Instrument.name == instrument_name).first()
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return db_instrument

@router.post("/", response_model=schemas.Instrument)
async def create_instrument(
    instrument: schemas.InstrumentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new instrument (admin only)"""
    try:
        instrument_data = instrument.dict()
        instrument_data['id'] = str(uuid.uuid4())
        db_instrument = crud.create_item(db, models.Instrument, instrument_data)
        
        # Send notification for new instrument
        from utils import send_content_notification
        await send_content_notification("instrument", instrument_data.get('name', 'Unknown'), instrument_data['id'])
        
        return db_instrument
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create instrument: {str(e)}")

@router.put("/{instrument_name}", response_model=schemas.Instrument)
async def update_instrument(instrument_name: str, instrument: schemas.InstrumentCreate, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)):
    """Update an instrument (admin only)"""
    db_instrument = db.query(models.Instrument).filter(models.Instrument.name == instrument_name).first()
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrument not found")
    instrument_data = instrument.dict()

    try:
        updated_instrument = crud.update_item(db, db_instrument, instrument_data)
        return updated_instrument
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update instrument: {str(e)}")

@router.delete("/{instrument_name}")
async def delete_instrument(instrument_name: str, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)):
    """Delete an instrument (admin only)"""
    db_instrument = db.query(models.Instrument).filter(models.Instrument.name == instrument_name).first()
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrument not found")

    try:
        crud.delete_item(db, db_instrument)
        return {"message": "Instrument deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete instrument: {str(e)}")