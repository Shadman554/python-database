from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import get_db
from auth import get_current_admin_user, security
import uuid
# Dependency function for admin authentication
def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    return get_current_admin_user(credentials, db)
router = APIRouter()

@router.get("/", response_model=schemas.About)
async def get_about(db: Session = Depends(get_db)):
    """Get about information"""
    try:
        about = db.query(models.About).first()
        if not about:
            raise HTTPException(status_code=404, detail="About information not found")
        return about
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve about information: {str(e)}")

@router.post("/", response_model=schemas.About)
async def create_about(
    about: schemas.AboutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Create about information (admin only)"""
    try:
        # Check if about already exists
        existing_about = db.query(models.About).first()
        if existing_about:
            raise HTTPException(status_code=400, detail="About information already exists. Use PUT to update.")
        
        about_data = about.dict()
        about_data['id'] = str(uuid.uuid4())
        db_about = crud.create_item(db, models.About, about_data)
        return db_about
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create about information: {str(e)}")

@router.put("/", response_model=schemas.About)
async def update_about(
    about: schemas.AboutCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Update about information (admin only)"""
    try:
        db_about = db.query(models.About).first()
        if not db_about:
            raise HTTPException(status_code=404, detail="About information not found")
        
        updated_about = crud.update_item(db, db_about, about.dict())
        return updated_about
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update about information: {str(e)}")

@router.delete("/")
async def delete_about(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    """Delete about information (admin only)"""
    try:
        db_about = db.query(models.About).first()
        if not db_about:
            raise HTTPException(status_code=404, detail="About information not found")
        
        crud.delete_item(db, db_about)
        return {"message": "About information deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete about information: {str(e)}")
