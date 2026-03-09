from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import get_db
from auth import get_current_user, get_current_admin_user, security
from utils import save_file, create_paginated_response
import uuid

# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get books with optional filtering and pagination"""
    try:
        if search:
            books = crud.search_books(db, search, skip, limit)
            total = crud.count_search_results(db, models.Book, search)
        elif category:
            books = crud.filter_books_by_category(db, category, skip, limit)
            total = db.query(models.Book).filter(models.Book.category == category).count()
        else:
            books = crud.get_items(db, models.Book, skip, limit)
            total = crud.count_items(db, models.Book)
        
        return create_paginated_response(books, total, skip // limit + 1, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve books: {str(e)}")

@router.get("/by-title/{book_title}", response_model=schemas.Book)
async def get_book_by_title(book_title: str, db: Session = Depends(get_db)):
    """Get a specific book by title"""
    book = db.query(models.Book).filter(models.Book.title.ilike(f"%{book_title}%")).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_title}", response_model=schemas.Book)
async def get_book(book_title: str, db: Session = Depends(get_db)):
    """Get a specific book by title"""
    book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create a new book (admin only)"""
    try:
        book_data = book.dict()
        book_data['id'] = str(uuid.uuid4())
        db_book = crud.create_item(db, models.Book, book_data)
        
        # Send push notification for new book
        from api.notifications import send_onesignal_notification
        await send_onesignal_notification(
            title="کتێبی نوێ",
            content=f"کتێبی نوێ زیادکراوە: {db_book.title}",
            custom_data={
                "book_id": db_book.id,
                "type": "new_book"
            }
        )
        
        return db_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")

@router.put("/{book_title}", response_model=schemas.Book)
async def update_book(
    book_title: str,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update a book (admin only)"""
    db_book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        updated_book = crud.update_item(db, db_book, book.dict())
        return updated_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update book: {str(e)}")

@router.delete("/{book_title}")
async def delete_book(
    book_title: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete a book (admin only)"""
    db_book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        crud.delete_item(db, db_book)
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete book: {str(e)}")

@router.post("/{book_title}/upload-cover")
async def upload_book_cover(
    book_title: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Upload book cover image (admin only)"""
    db_book = db.query(models.Book).filter(models.Book.title == book_title).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        file_url = await save_file(file, "covers")
        db_book.cover_url = file_url
        db.commit()
        return {"message": "Cover uploaded successfully", "cover_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload cover: {str(e)}")

@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique book categories"""
    try:
        categories = db.query(models.Book.category).distinct().all()
        return {"categories": [cat[0] for cat in categories if cat[0]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")
