
#!/usr/bin/env python3
"""
Create an admin user for testing
"""

from database import SessionLocal
from models import User
from auth import get_password_hash
import uuid

def create_admin_user():
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        admin_user = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@test.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_admin=True,
            total_points=0,
            today_points=0
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("You can now use this to test add/delete operations")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
