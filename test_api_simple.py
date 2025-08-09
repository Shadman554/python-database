#!/usr/bin/env python3
"""
Simple API test to identify the exact issue
"""

import requests
import json

BASE_URL = "https://python-database-production.up.railway.app"

def test_api_endpoints():
    """Test various API endpoints to identify the issue"""
    
    print("🔍 Testing API Endpoints")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get books (should work without auth)
    print("\n2. Testing get books...")
    try:
        response = requests.get(f"{BASE_URL}/api/books/")
        print(f"Get books status: {response.status_code}")
        if response.status_code == 200:
            books = response.json()
            print(f"Found {len(books.get('items', []))} books")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Try to create book without auth (should fail with 401/403)
    print("\n3. Testing create book without auth...")
    try:
        book_data = {
            "title": "Test Book",
            "description": "Test",
            "category": "test"
        }
        response = requests.post(f"{BASE_URL}/api/books/", json=book_data)
        print(f"Create book (no auth) status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Try to login (should fail if no admin user exists)
    print("\n4. Testing login...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        print(f"Login status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            print(f"Token received: {token_data.get('access_token', 'No token')[:50]}...")
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
