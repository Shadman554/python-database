#!/usr/bin/env python3
"""
Data Migration Script for Railway Database
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from import_data import main as import_data_main

def migrate_to_railway():
    """Migrate data to Railway PostgreSQL database"""
    
    # Get Railway database URL from environment
    railway_db_url = os.getenv('RAILWAY_DATABASE_URL') or os.getenv('DATABASE_URL')
    
    if not railway_db_url:
        print("Error: Please set RAILWAY_DATABASE_URL or DATABASE_URL environment variable")
        print("Get this from your Railway PostgreSQL service Variables tab")
        return
    
    print(f"Connecting to Railway database...")
    
    try:
        # Create engine and session
        engine = create_engine(railway_db_url)
        
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Import data
        print("Importing veterinary data...")
        import_data_main()
        
        print("✓ Data migration completed successfully!")
        print("Your Railway database is now ready with all veterinary data")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        print("Please check your database connection and try again")

if __name__ == "__main__":
    migrate_to_railway()