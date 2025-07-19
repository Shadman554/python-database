
#!/usr/bin/env python3
"""
Add sample data to the veterinary platform
"""
import requests
import json

# Your API base URL
API_BASE = "https://cbcb64e1-e448-4703-9f13-5c213ce880d6-00-1ngwve7l5udx6.sisko.replit.dev"

def login_admin():
    """Login and get admin token"""
    response = requests.post(f"{API_BASE}/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    return response.json()["access_token"]

def add_sample_books(token):
    """Add sample books"""
    headers = {"Authorization": f"Bearer {token}"}
    
    books = [
        {
            "title": "Veterinary Anatomy Basics",
            "description": "Complete guide to animal anatomy for veterinary students",
            "category": "Anatomy",
            "cover_url": "https://example.com/anatomy-book.jpg",
            "download_url": "https://example.com/anatomy-book.pdf"
        },
        {
            "title": "Small Animal Medicine",
            "description": "Comprehensive guide to small animal diseases and treatment",
            "category": "Medicine",
            "cover_url": "https://example.com/medicine-book.jpg",
            "download_url": "https://example.com/medicine-book.pdf"
        }
    ]
    
    for book in books:
        response = requests.post(f"{API_BASE}/api/books/", json=book, headers=headers)
        print(f"Added book: {book['title']} - Status: {response.status_code}")

def add_sample_diseases(token):
    """Add sample diseases"""
    headers = {"Authorization": f"Bearer {token}"}
    
    diseases = [
        {
            "name": "Canine Parvovirus",
            "kurdish": "ڤایرۆسی پارڤۆی سەگان",
            "symptoms": "Vomiting, diarrhea, lethargy, loss of appetite",
            "cause": "Parvovirus infection, highly contagious",
            "control": "Vaccination, isolation, supportive care"
        },
        {
            "name": "Feline Upper Respiratory Infection",
            "kurdish": "هەوکردنی سەرەوەی پشیلەکان",
            "symptoms": "Sneezing, nasal discharge, eye discharge, fever",
            "cause": "Viral or bacterial infection",
            "control": "Vaccination, antibiotics if bacterial, supportive care"
        }
    ]
    
    for disease in diseases:
        response = requests.post(f"{API_BASE}/api/diseases/", json=disease, headers=headers)
        print(f"Added disease: {disease['name']} - Status: {response.status_code}")

def add_sample_drugs(token):
    """Add sample drugs"""
    headers = {"Authorization": f"Bearer {token}"}
    
    drugs = [
        {
            "name": "Amoxicillin",
            "usage": "Antibiotic for bacterial infections",
            "side_effect": "Gastrointestinal upset, allergic reactions",
            "other_info": "Broad-spectrum penicillin antibiotic",
            "drug_class": "Antibiotic"
        },
        {
            "name": "Metacam",
            "usage": "Pain relief and anti-inflammatory",
            "side_effect": "GI upset, kidney issues with long-term use",
            "other_info": "NSAID commonly used in dogs and cats",
            "drug_class": "NSAID"
        }
    ]
    
    for drug in drugs:
        response = requests.post(f"{API_BASE}/api/drugs/", json=drug, headers=headers)
        print(f"Added drug: {drug['name']} - Status: {response.status_code}")

if __name__ == "__main__":
    print("🔐 Logging in as admin...")
    token = login_admin()
    print("✅ Login successful!")
    
    print("📚 Adding sample books...")
    add_sample_books(token)
    
    print("🦠 Adding sample diseases...")
    add_sample_diseases(token)
    
    print("💊 Adding sample drugs...")
    add_sample_drugs(token)
    
    print("✅ Sample data added successfully!")
