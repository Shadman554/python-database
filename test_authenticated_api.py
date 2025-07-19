#!/usr/bin/env python3
"""
Test authenticated API operations
"""

import requests
import json

BASE_URL = "https://python-database-production.up.railway.app"

def test_authenticated_operations():
    """Test login and authenticated book creation"""
    
    print("🔍 Testing Authenticated API Operations")
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print("✅ Login successful!")
            print(f"Token: {access_token[:50]}...")
            
            # Step 2: Create book with authentication
            print("\n2. Creating book with authentication...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            book_data = {
                "title": "Test Book via API",
                "description": "This book was created using authenticated API",
                "category": "test"
            }
            
            create_response = requests.post(
                f"{BASE_URL}/api/books/", 
                headers=headers, 
                json=book_data
            )
            
            print(f"Create book status: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            
            if create_response.status_code == 200:
                created_book = create_response.json()
                print("✅ Book created successfully!")
                print(f"Book ID: {created_book.get('id')}")
                print(f"Book Title: {created_book.get('title')}")
                
                # Step 3: Verify book exists
                print("\n3. Verifying book exists...")
                get_response = requests.get(f"{BASE_URL}/api/books/")
                if get_response.status_code == 200:
                    books = get_response.json()
                    book_titles = [book.get('title') for book in books.get('items', [])]
                    if "Test Book via API" in book_titles:
                        print("✅ Book found in database!")
                    else:
                        print("❌ Book not found in database")
                        print(f"Available books: {book_titles}")
                
            else:
                print(f"❌ Book creation failed")
                print(f"Status: {create_response.status_code}")
                print(f"Error: {create_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_authenticated_operations()
