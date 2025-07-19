
from database import SessionLocal
from models import User
from auth import get_password_hash
import uuid

def create_admin():
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    
    if admin:
        print("Admin user already exists!")
        return
    
    # Create admin user
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
    print("Username: admin")
    print("Password: admin123")
    
    db.close()

if __name__ == "__main__":
    create_admin()
