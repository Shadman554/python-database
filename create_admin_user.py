
#!/usr/bin/env python3
"""
Create an admin user for testing
"""
from database import SessionLocal
from models import User
from auth import get_password_hash
import uuid

def create_admin():
    db = SessionLocal()
    
    # Check if admin user already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("❌ Admin user already exists!")
        db.close()
        return
    
    # Create admin user
    admin_user = User(
        id=str(uuid.uuid4()),
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        is_admin=True,
        is_active=True,
        total_points=0,
        today_points=0
    )
    
    db.add(admin_user)
    db.commit()
    print("✅ Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
    db.close()

if __name__ == "__main__":
    create_admin()
