
#!/usr/bin/env python3
"""
Migration script to add photo_url column to users table
"""

from sqlalchemy import create_engine, text
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_add_photo_url():
    """Add photo_url column to users table"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='photo_url'
            """))
            
            if result.fetchone():
                logger.info("photo_url column already exists")
                return
            
            # Add the column
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN photo_url VARCHAR(1000)
            """))
            
            conn.commit()
            logger.info("Successfully added photo_url column to users table")
            
    except Exception as e:
        logger.error(f"Failed to add photo_url column: {e}")
        raise

if __name__ == "__main__":
    migrate_add_photo_url()
