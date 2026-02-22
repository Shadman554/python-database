from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_user, get_current_admin_user, security
from utils import create_paginated_response
import uuid
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/by-name/{word_name}", response_model=schemas.DictionaryWord)
async def get_word_by_name(word_name: str, db: Session = Depends(get_db)):
    """Get a specific dictionary word by name"""
    word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name.ilike(f"%{word_name}%")).first()
    if not word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")
    return word

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_dictionary_words(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None),
    favorites_only: bool = Query(False),
    saved_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Get dictionary words with optional filtering and pagination"""
    try:
        query = db.query(models.DictionaryWord)

        if search:
            query = query.filter(
                models.DictionaryWord.name.ilike(f"%{search}%") |
                models.DictionaryWord.kurdish.ilike(f"%{search}%") |
                models.DictionaryWord.arabic.ilike(f"%{search}%") |
                models.DictionaryWord.description.ilike(f"%{search}%")
            )

        if favorites_only:
            query = query.filter(models.DictionaryWord.is_favorite == True)

        if saved_only:
            query = query.filter(models.DictionaryWord.is_saved == True)

        total = query.count()
        words = query.offset(skip).limit(limit).all()

        return create_paginated_response(words, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dictionary words: {str(e)}")

@router.get("/{word_name}", response_model=schemas.DictionaryWord)
async def get_dictionary_word(word_name: str, db: Session = Depends(get_db)):
    """Get a specific dictionary word by name"""
    word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name == word_name).first()
    if not word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")
    return word

@router.post("/", response_model=schemas.DictionaryWord)
async def create_dictionary_word(
    word: schemas.DictionaryWordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new dictionary word (admin only)"""
    try:
        word_data = word.dict()
        word_data['id'] = str(uuid.uuid4())
        db_word = crud.create_item(db, models.DictionaryWord, word_data)
        
        # Send notification for new dictionary word
        from utils import send_content_notification
        await send_content_notification("word", word_data.get('name', 'Unknown'), word_data['id'])
        
        return db_word
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create dictionary word: {str(e)}")

@router.put("/{word_name}", response_model=schemas.DictionaryWord)
async def update_dictionary_word(
    word_name: str,
    word: schemas.DictionaryWordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a dictionary word (admin only)"""
    db_word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name == word_name).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")

    try:
        updated_word = crud.update_item(db, db_word, word.dict())
        return updated_word
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update dictionary word: {str(e)}")

@router.delete("/{word_name}")
async def delete_dictionary_word(
    word_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a dictionary word (admin only)"""
    db_word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name == word_name).first()
    if not db_word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")

    try:
        crud.delete_item(db, db_word)
        return {"message": "Dictionary word deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete dictionary word: {str(e)}")

def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    from auth import get_current_user
    return get_current_user(credentials, db)

@router.post("/{word_name}/favorite")
async def toggle_favorite(
    word_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_authenticated_user)
):
    """Toggle favorite status of a dictionary word"""
    word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name == word_name).first()
    if not word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")

    try:
        word.is_favorite = not word.is_favorite
        db.commit()

        # Award points for favoriting
        if word.is_favorite:
            crud.update_user_points(db, current_user.id, 1)

        return {"message": "Favorite status updated", "is_favorite": word.is_favorite}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update favorite status: {str(e)}")

@router.post("/{word_name}/save")
async def toggle_save(
    word_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_authenticated_user)
):
    """Toggle save status of a dictionary word"""
    word = db.query(models.DictionaryWord).filter(models.DictionaryWord.name == word_name).first()
    if not word:
        raise HTTPException(status_code=404, detail="Dictionary word not found")

    try:
        word.is_saved = not word.is_saved
        db.commit()

        # Award points for saving
        if word.is_saved:
            crud.update_user_points(db, current_user.id, 1)

        return {"message": "Save status updated", "is_saved": word.is_saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update save status: {str(e)}")