#!/usr/bin/env python3
"""
Create an admin user for testing
"""

from database import SessionLocal, Base, engine
from models import User
from auth import get_password_hash, pwd_context
import uuid
from datetime import datetime


def create_admin_user():
    """Create an admin user"""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists and delete it
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            print("Deleting existing admin user to recreate with compatible hash...")
            db.delete(admin_user)
            db.commit()
        
        # Create admin user with fresh hash
        hashed_password = get_password_hash("admin123")
        print(f"Generated hash: {hashed_password[:50]}...")
        
        admin_user = User(
            id="admin-" + str(uuid.uuid4()),
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True,
            total_points=0,
            today_points=0,
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        
        # Test the hash verification
        test_verify = pwd_context.verify("admin123", hashed_password)
        print(f"Hash verification test: {test_verify}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()