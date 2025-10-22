from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import models
import schemas
from datetime import datetime
import uuid
from auth import verify_password, get_password_hash

# Generic CRUD operations
def get_item(db: Session, model, item_id: str):
    return db.query(model).filter(model.id == item_id).first()

def get_items(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()

def create_item(db: Session, model, item_data: dict):
    if 'id' not in item_data:
        item_data['id'] = str(uuid.uuid4())
    db_item = model(**item_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item, item_data: dict):
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item):
    db.delete(db_item)
    db.commit()

# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        photo_url=user.photo_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_points(db: Session, user_id: str, points: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.total_points += points
        user.today_points += points
        user.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(user)
    return user

# Search functions
def search_books(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(
        or_(
            models.Book.title.ilike(f"%{query}%"),
            models.Book.description.ilike(f"%{query}%"),
            models.Book.category.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

def search_diseases(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.Disease).filter(
        or_(
            models.Disease.name.ilike(f"%{query}%"),
            models.Disease.kurdish.ilike(f"%{query}%"),
            models.Disease.symptoms.ilike(f"%{query}%"),
            models.Disease.cause.ilike(f"%{query}%"),
            models.Disease.control.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

def search_drugs(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.Drug).filter(
        or_(
            models.Drug.name.ilike(f"%{query}%"),
            models.Drug.usage.ilike(f"%{query}%"),
            models.Drug.drug_class.ilike(f"%{query}%"),
            models.Drug.trade_names.ilike(f"%{query}%"),
            models.Drug.species_dosages.ilike(f"%{query}%"),
            models.Drug.contraindications.ilike(f"%{query}%"),
            models.Drug.drug_interactions.ilike(f"%{query}%"),
            models.Drug.withdrawal_times.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

def search_dictionary(db: Session, query: str, skip: int = 0, limit: int = 100):
    return db.query(models.DictionaryWord).filter(
        or_(
            models.DictionaryWord.name.ilike(f"%{query}%"),
            models.DictionaryWord.kurdish.ilike(f"%{query}%"),
            models.DictionaryWord.arabic.ilike(f"%{query}%"),
            models.DictionaryWord.description.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

# Filter functions
def filter_books_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.category == category).offset(skip).limit(limit).all()

def filter_drugs_by_class(db: Session, drug_class: str, skip: int = 0, limit: int = 100):
    return db.query(models.Drug).filter(models.Drug.drug_class == drug_class).offset(skip).limit(limit).all()

def filter_normal_ranges_by_species(db: Session, species: str, skip: int = 0, limit: int = 100):
    return db.query(models.NormalRange).filter(models.NormalRange.species == species).offset(skip).limit(limit).all()

def filter_normal_ranges_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(models.NormalRange).filter(models.NormalRange.category == category).offset(skip).limit(limit).all()

# Count functions
def count_items(db: Session, model):
    return db.query(model).count()

def count_search_results(db: Session, model, query: str):
    if model == models.Book:
        return db.query(model).filter(
            or_(
                models.Book.title.ilike(f"%{query}%"),
                models.Book.description.ilike(f"%{query}%"),
                models.Book.category.ilike(f"%{query}%")
            )
        ).count()
    elif model == models.Disease:
        return db.query(model).filter(
            or_(
                models.Disease.name.ilike(f"%{query}%"),
                models.Disease.kurdish.ilike(f"%{query}%"),
                models.Disease.symptoms.ilike(f"%{query}%"),
                models.Disease.cause.ilike(f"%{query}%"),
                models.Disease.control.ilike(f"%{query}%")
            )
        ).count()
    elif model == models.Drug:
        return db.query(model).filter(
            or_(
                models.Drug.name.ilike(f"%{query}%"),
                models.Drug.usage.ilike(f"%{query}%"),
                models.Drug.drug_class.ilike(f"%{query}%"),
                models.Drug.trade_names.ilike(f"%{query}%"),
                models.Drug.species_dosages.ilike(f"%{query}%"),
                models.Drug.contraindications.ilike(f"%{query}%"),
                models.Drug.drug_interactions.ilike(f"%{query}%"),
                models.Drug.withdrawal_times.ilike(f"%{query}%")
            )
        ).count()
    elif model == models.DictionaryWord:
        return db.query(model).filter(
            or_(
                models.DictionaryWord.name.ilike(f"%{query}%"),
                models.DictionaryWord.kurdish.ilike(f"%{query}%"),
                models.DictionaryWord.arabic.ilike(f"%{query}%"),
                models.DictionaryWord.description.ilike(f"%{query}%")
            )
        ).count()
    return 0