#!/usr/bin/env python3
"""
Simple test to check database write operations
"""

import models
from database import SessionLocal
from sqlalchemy import text
import uuid

def test_database_operations():
    print('Testing database operations...')
    db = SessionLocal()

    try:
        # Check if tables exist
        tables = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")).fetchall()
        print(f'Tables: {[t[0] for t in tables]}')
        
        # Check if books table has data
        book_count = db.execute(text("SELECT COUNT(*) FROM books")).fetchone()
        print(f'Books in database: {book_count[0]}')
        
        # Test creating a book
        test_book = models.Book(
            id=str(uuid.uuid4()),
            title='TEST_BOOK_DELETE_ME',
            description='Test book for write operations',
            category='test'
        )
        db.add(test_book)
        db.commit()
        print('✅ Book created successfully')
        
        # Verify it was created
        created_book = db.query(models.Book).filter(models.Book.title == 'TEST_BOOK_DELETE_ME').first()
        if created_book:
            print(f'✅ Book found: {created_book.title}')
        
        # Clean up
        db.delete(test_book)
        db.commit()
        print('✅ Book deleted successfully')
        
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_database_operations()
    if success:
        print('\n✅ All database operations work correctly!')
        print('The issue might be with API authentication or request handling.')
    else:
        print('\n❌ Database write operations failed.')
