#!/usr/bin/env python3
"""
Create admin user for the veterinary platform
"""

import models
import schemas
import crud
from database import SessionLocal
from auth import get_password_hash
import uuid

def create_admin_user():
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            print(f"Is Admin: {existing_admin.is_admin}")
            return existing_admin
        
        # Create admin user
        admin_data = {
            'id': str(uuid.uuid4()),
            'username': 'admin',
            'email': 'admin@veterinary.com',
            'hashed_password': get_password_hash('admin123'),
            'is_admin': True,
            'is_active': True
        }
        
        admin_user = models.User(**admin_data)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"Username: {admin_user.username}")
        print(f"Password: admin123")
        print(f"Email: {admin_user.email}")
        print(f"Is Admin: {admin_user.is_admin}")
        
        return admin_user
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
