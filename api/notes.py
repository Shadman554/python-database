
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
async def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all notes with pagination"""
    try:
        notes = db.query(models.Note).order_by(models.Note.created_at.desc()).offset(skip).limit(limit).all()
        total = crud.count_items(db, models.Note)
        return create_paginated_response(notes, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notes: {str(e)}")

@router.get("/{note_id}", response_model=schemas.Note)
async def get_note(note_id: str, db: Session = Depends(get_db)):
    """Get a specific note by ID"""
    note = crud.get_item(db, models.Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/", response_model=schemas.Note)
async def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Create a new note (admin only)"""
    try:
        note_data = note.dict()
        note_data['id'] = str(uuid.uuid4())
        db_note = crud.create_item(db, models.Note, note_data)
        return db_note
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")

@router.put("/{note_id}", response_model=schemas.Note)
async def update_note(
    note_id: str,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Update a note (admin only)"""
    db_note = crud.get_item(db, models.Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    try:
        updated_note = crud.update_item(db, db_note, note.dict())
        return updated_note
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update note: {str(e)}")

@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(lambda: get_current_admin_user(security, db))
):
    """Delete a note (admin only)"""
    db_note = crud.get_item(db, models.Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    try:
        crud.delete_item(db, db_note)
        return {"message": "Note deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete note: {str(e)}")
