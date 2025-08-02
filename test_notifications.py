
#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://python-database-production.up.railway.app"

def test_notification_creation():
    """Test creating notifications that trigger OneSignal"""
    
    # Login first
    login_data = {"username": "admin", "password": "admin123"}
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test direct notification creation
        notification_data = {
            "title": "تاقیکردنەوە",
            "content": "ئەمە تاقیکردنەوەیەکە بۆ OneSignal",
            "type": "test"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/notifications/",
            headers=headers,
            json=notification_data
        )
        
        print(f"Notification creation status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Notification sent successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    test_notification_creation()
