
#!/usr/bin/env python3

print("Testing all imports...")

try:
    import fastapi
    print("✅ FastAPI imported")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")

try:
    import sqlalchemy
    print("✅ SQLAlchemy imported")
except ImportError as e:
    print(f"❌ SQLAlchemy import failed: {e}")

try:
    import uvicorn
    print("✅ Uvicorn imported")
except ImportError as e:
    print(f"❌ Uvicorn import failed: {e}")

try:
    from config import settings
    print(f"✅ Config imported, DATABASE_URL: {settings.DATABASE_URL[:50]}...")
except Exception as e:
    print(f"❌ Config import failed: {e}")

try:
    from database import engine
    print("✅ Database engine imported")
except Exception as e:
    print(f"❌ Database import failed: {e}")

try:
    from models import Base
    print("✅ Models imported")
except Exception as e:
    print(f"❌ Models import failed: {e}")

try:
    from auth import verify_token
    print("✅ Auth imported")
except Exception as e:
    print(f"❌ Auth import failed: {e}")

print("Import test completed!")
