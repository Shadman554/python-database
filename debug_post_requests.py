
#!/usr/bin/env python3
"""
Debug POST requests to identify why data isn't being saved to PostgreSQL
"""

import requests
import json
from database import get_db, SessionLocal
from models import User, Book, Disease, Drug
from auth import get_password_hash
import uuid

def test_database_write():
    """Test direct database write operations"""
    db = SessionLocal()
    
    try:
        print("🔧 Testing direct database write...")
        
        # Test creating a book directly
        test_book = Book(
            id=str(uuid.uuid4()),
            title="Test Book Direct",
            description="Testing direct database write",
            category="Test"
        )
        
        db.add(test_book)
        db.commit()
        db.refresh(test_book)
        
        print(f"✅ Direct write successful: {test_book.title}")
        
        # Clean up
        db.delete(test_book)
        db.commit()
        print("🧹 Cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct write failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

def test_api_post():
    """Test API POST request"""
    API_BASE = "http://0.0.0.0:5000"
    
    try:
        print("🌐 Testing API POST request...")
        
        # First, try to login and get token
        login_data = {
            "username": "admin",  # Adjust if different
            "password": "admin123"  # Adjust if different
        }
        
        response = requests.post(f"{API_BASE}/api/auth/login", data=login_data)
        print(f"Login response: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test creating a book via API
            book_data = {
                "title": "Test Book API",
                "description": "Testing API POST",
                "category": "Test"
            }
            
            book_response = requests.post(f"{API_BASE}/api/books/", json=book_data, headers=headers)
            print(f"Book creation response: {book_response.status_code}")
            print(f"Response content: {book_response.text}")
            
            if book_response.status_code == 201:
                print("✅ API POST successful")
                return True
            else:
                print("❌ API POST failed")
                return False
        else:
            print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def check_database_connection():
    """Check database connection and tables"""
    db = SessionLocal()
    
    try:
        print("📊 Checking database connection...")
        
        # Test basic query
        books_count = db.query(Book).count()
        print(f"Current books count: {books_count}")
        
        diseases_count = db.query(Disease).count()
        print(f"Current diseases count: {diseases_count}")
        
        drugs_count = db.query(Drug).count()
        print(f"Current drugs count: {drugs_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=== POST Request Debugging ===")
    
    # Test 1: Database connection
    if not check_database_connection():
        print("Database connection failed. Check your DATABASE_URL.")
        exit(1)
    
    # Test 2: Direct database write
    if not test_database_write():
        print("Direct database write failed. Check your database permissions.")
        exit(1)
    
    # Test 3: API POST request
    print("\n📱 Starting FastAPI server for API testing...")
    print("Please run 'python main.py' in another terminal, then run this script again with --api-only flag")
    
    import sys
    if "--api-only" in sys.argv:
        test_api_post()
