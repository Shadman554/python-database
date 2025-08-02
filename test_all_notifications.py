
#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "https://python-database-production.up.railway.app"

def get_admin_token():
    """Get admin authentication token"""
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Failed to login: {response.text}")
        return None

def test_content_notifications(token):
    """Test notifications for all content types"""
    headers = {"Authorization": f"Bearer {token}"}
    
    test_cases = [
        {
            "endpoint": "/api/books/",
            "data": {
                "title": "کتێبی تاقیکردنەوە",
                "description": "ئەمە کتێبێکی تاقیکردنەوەیە",
                "type": "test"
            },
            "name": "Book"
        },
        {
            "endpoint": "/api/diseases/",
            "data": {
                "name": "نەخۆشی تاقیکردنەوە",
                "symptoms": "نیشانەکانی تاقیکردنەوە",
                "control": "کۆنترۆڵی تاقیکردنەوە"
            },
            "name": "Disease"
        },
        {
            "endpoint": "/api/drugs/",
            "data": {
                "name": "دەرمانی تاقیکردنەوە",
                "usage": "بەکارهێنانی تاقیکردنەوە",
                "sideEffect": "کاریگەری لاوەکی تاقیکردنەوە"
            },
            "name": "Drug"
        },
        {
            "endpoint": "/api/dictionary/",
            "data": {
                "name": "Test Word",
                "kurdish": "وشەی تاقیکردنەوە",
                "description": "پێناسەی تاقیکردنەوە"
            },
            "name": "Dictionary Word"
        },
        {
            "endpoint": "/api/instruments/",
            "data": {
                "name": "ئامێری تاقیکردنەوە",
                "description": "پێناسەی ئامێری تاقیکردنەوە"
            },
            "name": "Instrument"
        },
        {
            "endpoint": "/api/notes/",
            "data": {
                "name": "تێبینی تاقیکردنەوە",
                "description": "ناوەڕۆکی تێبینی تاقیکردنەوە"
            },
            "name": "Note"
        }
    ]
    
    print("🧪 Testing automatic notifications for content creation...")
    
    for test_case in test_cases:
        print(f"\n📝 Testing {test_case['name']} creation...")
        
        response = requests.post(
            f"{BASE_URL}{test_case['endpoint']}",
            headers=headers,
            json=test_case["data"]
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ {test_case['name']} created successfully")
            print(f"   OneSignal notification should be sent automatically")
        else:
            print(f"❌ Failed to create {test_case['name']}: {response.status_code}")
            print(f"   Error: {response.text}")
        
        time.sleep(1)  # Small delay between requests

def test_manual_notification(token):
    """Test manual notification creation"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📢 Testing manual notification creation...")
    
    notification_data = {
        "title": "ئاگاداری تاقیکردنەوە",
        "body": "ئەمە ئاگاداری تاقیکردنەوەیەکە بۆ OneSignal",
        "type": "manual_test"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/notifications/",
        headers=headers,
        json=notification_data
    )
    
    if response.status_code in [200, 201]:
        print("✅ Manual notification created successfully")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Failed to create manual notification: {response.status_code}")
        print(f"   Error: {response.text}")

def check_recent_notifications():
    """Check recent notifications"""
    print("\n📋 Checking recent notifications...")
    
    response = requests.get(f"{BASE_URL}/api/notifications/recent/latest?limit=10")
    
    if response.status_code == 200:
        notifications = response.json()["notifications"]
        print(f"✅ Found {len(notifications)} recent notifications:")
        
        for i, notif in enumerate(notifications[:5], 1):
            print(f"   {i}. {notif['title']} - {notif['body'][:50]}...")
    else:
        print(f"❌ Failed to fetch notifications: {response.status_code}")

def main():
    print("🚀 Starting comprehensive notification system test...\n")
    
    # Get authentication token
    token = get_admin_token()
    if not token:
        return
    
    print("✅ Successfully authenticated as admin\n")
    
    # Test content creation notifications
    test_content_notifications(token)
    
    # Test manual notification
    test_manual_notification(token)
    
    # Check recent notifications
    time.sleep(2)  # Wait a bit for notifications to be processed
    check_recent_notifications()
    
    print("\n🎉 Notification system testing completed!")
    print("\n💡 Next steps:")
    print("   1. Check your OneSignal dashboard for sent notifications")
    print("   2. Test on your mobile app to verify push notifications")
    print("   3. Monitor notification delivery rates")

if __name__ == "__main__":
    main()
