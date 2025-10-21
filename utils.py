from fastapi import HTTPException, UploadFile
from typing import List, Any
import os
import uuid
import shutil
from config import settings

def create_paginated_response(items, total, page, size):
    """Create a paginated response"""
    # Convert SQLAlchemy objects to dictionaries for proper serialization
    serialized_items = []
    for item in items:
        if hasattr(item, '__dict__'):
            # Convert SQLAlchemy object to dict, excluding private attributes
            item_dict = {key: value for key, value in item.__dict__.items() 
                        if not key.startswith('_')}
            serialized_items.append(item_dict)
        else:
            serialized_items.append(item)

    return {
        "items": serialized_items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

async def save_file(file: UploadFile, folder: str) -> str:
    """Save uploaded file and return file URL"""
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Create upload directory if it doesn't exist
    upload_path = os.path.join(settings.UPLOAD_DIR, folder)
    os.makedirs(upload_path, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_path, unique_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return file URL (adjust this based on your file serving setup)
        return f"/uploads/{folder}/{unique_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

def validate_file_size(file: UploadFile) -> bool:
    """Validate file size"""
    if file.size > settings.MAX_FILE_SIZE:
        return False
    return True

def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return os.path.splitext(filename)[1].lower()

def generate_unique_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())

def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    # Remove or replace problematic characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def format_search_query(query: str) -> str:
    """Format search query for database"""
    # Remove extra whitespace and convert to lowercase
    return query.strip().lower()

def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (basic implementation)"""
    if not str1 or not str2:
        return 0.0

    # Convert to lowercase for comparison
    str1, str2 = str1.lower(), str2.lower()

    # Simple similarity based on common characters
    common_chars = set(str1) & set(str2)
    total_chars = set(str1) | set(str2)

    if not total_chars:
        return 0.0

    return len(common_chars) / len(total_chars)

async def send_content_notification(content_type: str, title: str, item_id: str):
    """Send notification for new content"""
    from api.notifications import send_onesignal_notification
    
    notification_titles = {
        "book": "کتێبی نوێ",
        "disease": "نەخۆشی نوێ", 
        "drug": "دەرمانی نوێ",
        "question": "پرسیاری نوێ",
        "word": "وشەی نوێ",
        "instrument": "ئامێری نوێ",
        "note": "تێبینی نوێ",
        "slide": "سلایدی نوێ",
        "haematology_test": "پشکنینی نوێ",
        "serology_test": "پشکنینی نوێ",
        "biochemistry_test": "پشکنینی نوێ",
        "bacteriology_test": "پشکنینی نوێ",
        "other_test": "پشکنینی نوێ"
    }
    
    notification_title = notification_titles.get(content_type, "ناوەڕۆکی نوێ")
    
    await send_onesignal_notification(
        title=notification_title,
        content=f"{notification_title} زیادکراوە: {title}",
        custom_data={
            f"{content_type}_id": item_id,
            "type": f"new_{content_type}"
        }
    )