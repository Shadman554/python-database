
import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Disease

def test_diseases_import():
    """Test diseases import with detailed debugging"""
    db = SessionLocal()
    
    try:
        # Test database connection
        print("Testing database connection...")
        current_count = db.query(Disease).count()
        print(f"✓ Current diseases in database: {current_count}")
        
        # Test JSON file reading
        print("\nTesting JSON file...")
        with open('attached_assets/diseases_1752089134448.json', 'r', encoding='utf-8') as f:
            diseases_data = json.load(f)
        print(f"✓ JSON file contains {len(diseases_data)} diseases")
        
        # Check first disease structure
        if diseases_data:
            first_disease = diseases_data[0]
            print(f"✓ First disease structure: {list(first_disease.keys())}")
            print(f"✓ First disease name: {first_disease.get('name', 'No name')}")
        
        # Try to add one test disease
        print("\nTesting single disease insertion...")
        test_disease_data = diseases_data[0]
        test_id = f"test_{test_disease_data['id']}"
        
        # Check if test disease exists
        existing = db.query(Disease).filter(Disease.id == test_id).first()
        if existing:
            print(f"Removing existing test disease...")
            db.delete(existing)
            db.commit()
        
        test_disease = Disease(
            id=test_id,
            name=test_disease_data.get('name', ''),
            kurdish=test_disease_data.get('kurdish', ''),
            symptoms=test_disease_data.get('symptoms', ''),
            cause=test_disease_data.get('cause', ''),
            control=test_disease_data.get('control', ''),
            created_at=datetime.utcnow()
        )
        
        db.add(test_disease)
        db.commit()
        print(f"✓ Successfully added test disease")
        
        # Verify test disease was added
        verify = db.query(Disease).filter(Disease.id == test_id).first()
        if verify:
            print(f"✓ Test disease verified in database: {verify.name}")
            # Clean up
            db.delete(verify)
            db.commit()
            print("✓ Test disease cleaned up")
        else:
            print("❌ Test disease not found after insertion")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_diseases_import()
