#!/usr/bin/env python3
"""
Create admin user for the veterinary platform.

Usage:
    ADMIN_USERNAME=myuser ADMIN_EMAIL=me@example.com ADMIN_PASSWORD=StrongPass! python create_admin.py

Required environment variables:
    ADMIN_PASSWORD  - Strong password for the admin account (min 12 chars)
Optional:
    ADMIN_USERNAME  - Defaults to 'admin'
    ADMIN_EMAIL     - Defaults to 'admin@veterinary.com'
"""

import os
import sys
import uuid
from database import SessionLocal, engine
from models import Base, User
from auth import get_password_hash


def create_admin_user():
    """Create an admin user using credentials from environment variables."""

    admin_password = os.getenv('ADMIN_PASSWORD', '')
    if not admin_password:
        print("❌ ERROR: ADMIN_PASSWORD environment variable is required.")
        print("   Set it before running: ADMIN_PASSWORD=YourStrongPassword python create_admin.py")
        sys.exit(1)

    if len(admin_password) < 12:
        print("❌ ERROR: ADMIN_PASSWORD must be at least 12 characters long.")
        sys.exit(1)

    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_email    = os.getenv('ADMIN_EMAIL', 'admin@veterinary.com')

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(
            (User.username == admin_username) | (User.email == admin_email)
        ).first()

        if existing:
            print(f"✅ Admin user already exists (username: {existing.username}).")
            return

        admin_user = User(
            id=str(uuid.uuid4()),
            username=admin_username,
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            is_admin=True,
            is_active=True,
        )

        db.add(admin_user)
        db.commit()

        print("✅ Admin user created successfully.")
        print(f"   Username : {admin_username}")
        print(f"   Email    : {admin_email}")
        print("   Password : (set via ADMIN_PASSWORD env var)")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
