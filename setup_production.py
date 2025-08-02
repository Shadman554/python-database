
#!/usr/bin/env python3
"""
Production setup script for Replit deployment
"""

import os
import json
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Book, Disease, Drug, DictionaryWord, User, Question, Notification, Staff, NormalRange, AppLink, About
import hashlib

def convert_timestamp(timestamp_obj):
    """Convert Firebase timestamp to datetime"""
    if isinstance(timestamp_obj, dict) and '_seconds' in timestamp_obj:
        return datetime.fromtimestamp(timestamp_obj['_seconds'])
    return datetime.utcnow()

def create_admin_user(db: Session):
    """Create default admin user"""
    admin_email = "admin@veterinary.app"
    admin_password = "admin123"  # Change this in production
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    if existing_admin:
        print("✓ Admin user already exists")
        return existing_admin
    
    # Hash password
    hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()
    
    admin_user = User(
        id="admin-001",
        name="Admin",
        email=admin_email,
        password_hash=hashed_password,
        role="admin",
        points=0,
        photo_url=None
    )
    
    db.add(admin_user)
    db.commit()
    print(f"✓ Created admin user: {admin_email} / {admin_password}")
    return admin_user

def import_production_data():
    """Import all data for production"""
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Setting up production database...")
        
        # Create admin user
        create_admin_user(db)
        
        # Import books if file exists
        try:
            with open('attached_assets/books_1752089134448.json', 'r', encoding='utf-8') as f:
                books_data = json.load(f)
            
            imported_books = 0
            for book_data in books_data:
                existing_book = db.query(Book).filter(Book.id == book_data['id']).first()
                if not existing_book:
                    book = Book(
                        id=book_data['id'],
                        title=book_data.get('title', ''),
                        description=book_data.get('description', ''),
                        category=book_data.get('category', ''),
                        cover_url=book_data.get('coverUrl', ''),
                        download_url=book_data.get('downloadUrl', ''),
                        added_at=convert_timestamp(book_data.get('addedAt', {}))
                    )
                    db.add(book)
                    imported_books += 1
            
            db.commit()
            print(f"✓ Imported {imported_books} books")
        except FileNotFoundError:
            print("⚠️  Books data file not found, skipping...")
        except Exception as e:
            print(f"Error importing books: {e}")
        
        # Import diseases if file exists
        try:
            with open('attached_assets/diseases_1752089134448.json', 'r', encoding='utf-8') as f:
                diseases_data = json.load(f)
            
            imported_diseases = 0
            for disease_data in diseases_data:
                existing_disease = db.query(Disease).filter(Disease.id == disease_data['id']).first()
                if not existing_disease:
                    disease = Disease(
                        id=disease_data['id'],
                        name=disease_data.get('name', ''),
                        kurdish=disease_data.get('kurdish', ''),
                        arabic=disease_data.get('arabic', ''),
                        description=disease_data.get('description', ''),
                        symptoms=disease_data.get('symptoms', ''),
                        treatment=disease_data.get('treatment', ''),
                        category=disease_data.get('category', ''),
                        image_url=disease_data.get('imageUrl', ''),
                        added_at=convert_timestamp(disease_data.get('addedAt', {}))
                    )
                    db.add(disease)
                    imported_diseases += 1
            
            db.commit()
            print(f"✓ Imported {imported_diseases} diseases")
        except FileNotFoundError:
            print("⚠️  Diseases data file not found, skipping...")
        except Exception as e:
            print(f"Error importing diseases: {e}")
        
        # Import drugs if file exists
        try:
            with open('attached_assets/drugs_1752089134449.json', 'r', encoding='utf-8') as f:
                drugs_data = json.load(f)
            
            imported_drugs = 0
            for drug_data in drugs_data:
                existing_drug = db.query(Drug).filter(Drug.id == drug_data['id']).first()
                if not existing_drug:
                    drug = Drug(
                        id=drug_data['id'],
                        name=drug_data.get('name', ''),
                        kurdish=drug_data.get('kurdish', ''),
                        arabic=drug_data.get('arabic', ''),
                        description=drug_data.get('description', ''),
                        dosage=drug_data.get('dosage', ''),
                        side_effects=drug_data.get('sideEffects', ''),
                        category=drug_data.get('category', ''),
                        image_url=drug_data.get('imageUrl', ''),
                        added_at=convert_timestamp(drug_data.get('addedAt', {}))
                    )
                    db.add(drug)
                    imported_drugs += 1
            
            db.commit()
            print(f"✓ Imported {imported_drugs} drugs")
        except FileNotFoundError:
            print("⚠️  Drugs data file not found, skipping...")
        except Exception as e:
            print(f"Error importing drugs: {e}")
        
        # Show final counts
        books_count = db.query(Book).count()
        diseases_count = db.query(Disease).count()
        drugs_count = db.query(Drug).count()
        users_count = db.query(User).count()
        
        print(f"\n📊 Production Database Status:")
        print(f"  - Books: {books_count}")
        print(f"  - Diseases: {diseases_count}")
        print(f"  - Drugs: {drugs_count}")
        print(f"  - Users: {users_count}")
        print(f"  - Total Records: {books_count + diseases_count + drugs_count + users_count}")
        
        print("\n✅ Production setup completed successfully!")
        print("Your app is ready for deployment!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_production_data()
