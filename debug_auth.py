
#!/usr/bin/env python3
"""
Debug authentication and database operations
"""
import requests
import json
from database import get_db, SessionLocal
from models import User, Book, Disease, Drug
from auth import get_password_hash
import uuid

def test_login_and_create():
    """Test login and create operations"""
    
    # First, let's create a test admin user if needed
    db = SessionLocal()
    
    # Check if admin user exists
    admin_user = db.query(User).filter(User.is_admin == True).first()
    
    if not admin_user:
        print("Creating admin user...")
        admin_user = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✅ Admin user created!")
    else:
        print(f"✅ Admin user exists: {admin_user.username}")
    
    db.close()
    
    # Test login
    base_url = "http://0.0.0.0:5000"
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print("\n🔐 Testing login...")
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful!")
            
            # Test creating a book
            headers = {"Authorization": f"Bearer {token}"}
            book_data = {
                "title": "Test Book",
                "description": "Test Description",
                "category": "Test Category"
            }
            
            print("\n📚 Testing book creation...")
            book_response = requests.post(
                f"{base_url}/api/books/", 
                json=book_data, 
                headers=headers
            )
            print(f"Book creation response: {book_response.status_code}")
            if book_response.status_code == 200:
                print("✅ Book created successfully!")
                print(f"Book: {book_response.json()}")
            else:
                print(f"❌ Book creation failed: {book_response.text}")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login_and_create()
