
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Book, Disease, Drug
from auth import get_password_hash
import json

# Use local SQLite for development
DATABASE_URL = "sqlite:///./local_dev.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_local_database():
    """Set up local development database with sample data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create a test admin user
        admin_user = User(
            id="admin-123",
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            is_admin=True,
            points=0
        )
        db.add(admin_user)
        
        # Create a test regular user
        test_user = User(
            id="user-123",
            username="testuser",
            email="test@example.com",
            password_hash=get_password_hash("test123"),
            is_admin=False,
            points=100
        )
        db.add(test_user)
        
        # Add some sample books
        sample_book = Book(
            id="book-1",
            title="Veterinary Medicine Basics",
            description="A comprehensive guide to veterinary medicine",
            category="Education",
            cover_url="https://example.com/cover.jpg",
            download_url="https://example.com/book.pdf"
        )
        db.add(sample_book)
        
        # Add some sample diseases
        sample_disease = Disease(
            id="disease-1",
            name="Rabies",
            description="A viral disease affecting the nervous system",
            symptoms="Aggression, paralysis, hydrophobia",
            treatment="Post-exposure prophylaxis, vaccination",
            prevention="Vaccination, avoid contact with wild animals"
        )
        db.add(sample_disease)
        
        # Add some sample drugs
        sample_drug = Drug(
            id="drug-1",
            name="Penicillin",
            description="Antibiotic medication",
            dosage="10mg/kg body weight",
            administration="Intramuscular injection",
            contraindications="Allergy to penicillin"
        )
        db.add(sample_drug)
        
        db.commit()
        print("✓ Local development database created successfully!")
        print("✓ Sample data added")
        print("\nTest users created:")
        print("- Admin: username='admin', password='admin123'")
        print("- User: username='testuser', password='test123'")
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_local_database()
