#!/usr/bin/env python3
"""
Test API write operations with authentication
"""

import requests
import json

# API base URL
BASE_URL = "https://python-database-production.up.railway.app"

def test_api_operations():
    """Test API login and write operations"""
    
    print("🔍 Testing API Write Operations")
    print(f"API URL: {BASE_URL}")
    
    # Step 1: Login to get JWT token
    print("\n1. Testing login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print("✅ Login successful!")
            print(f"Token: {access_token[:50]}...")
            
            # Step 2: Test creating a book
            print("\n2. Testing book creation...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            book_data = {
                "title": "Test Book API",
                "description": "This is a test book created via API",
                "category": "test",
                "author": "API Test",
                "pages": 100
            }
            
            create_response = requests.post(
                f"{BASE_URL}/api/books/", 
                headers=headers, 
                json=book_data
            )
            
            print(f"Create book status: {create_response.status_code}")
            if create_response.status_code == 200:
                created_book = create_response.json()
                print("✅ Book created successfully!")
                print(f"Book ID: {created_book.get('id')}")
                print(f"Book Title: {created_book.get('title')}")
                
                # Step 3: Test updating the book
                print("\n3. Testing book update...")
                update_data = {
                    "title": "Updated Test Book API",
                    "description": "This book was updated via API",
                    "category": "updated",
                    "author": "API Test Updated",
                    "pages": 150
                }
                
                update_response = requests.put(
                    f"{BASE_URL}/api/books/Test Book API",
                    headers=headers,
                    json=update_data
                )
                
                print(f"Update book status: {update_response.status_code}")
                if update_response.status_code == 200:
                    print("✅ Book updated successfully!")
                else:
                    print(f"❌ Book update failed: {update_response.text}")
                
                # Step 4: Test deleting the book
                print("\n4. Testing book deletion...")
                delete_response = requests.delete(
                    f"{BASE_URL}/api/books/Updated Test Book API",
                    headers=headers
                )
                
                print(f"Delete book status: {delete_response.status_code}")
                if delete_response.status_code == 200:
                    print("✅ Book deleted successfully!")
                else:
                    print(f"❌ Book deletion failed: {delete_response.text}")
                    
            else:
                print(f"❌ Book creation failed: {create_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_operations()
