
import os
import psycopg2
from urllib.parse import urlparse

def test_database_connection():
    """Test database connection with detailed error reporting"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ No DATABASE_URL environment variable found")
        print("Please set your Railway database URL in the .env file")
        return False
    
    print(f"📡 Testing connection to database...")
    
    # Parse the URL to show connection details (without password)
    try:
        parsed = urlparse(database_url)
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"Database: {parsed.path[1:] if parsed.path else 'N/A'}")
        print(f"Username: {parsed.username}")
        
        # Check if it's an internal Railway URL
        if 'railway.internal' in parsed.hostname:
            print("⚠️  WARNING: This appears to be an internal Railway URL")
            print("   You need the PUBLIC/EXTERNAL database URL from Railway")
            print("   Go to Railway Dashboard > PostgreSQL service > Variables tab")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False
    
    # Test the actual connection
    try:
        print("🔗 Attempting to connect...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Test a simple query
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"✅ Connection successful!")
        print(f"PostgreSQL version: {version}")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure you're using the PUBLIC database URL from Railway")
        print("2. Check that the database service is running in Railway")
        print("3. Verify the URL is correctly set in your .env file")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
