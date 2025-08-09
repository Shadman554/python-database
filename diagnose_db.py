#!/usr/bin/env python3
"""
Database Diagnostic Script
This script helps diagnose database connectivity and permission issues
"""

import sys
import logging
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from config import settings
import models
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_connection():
    """Test basic database connectivity"""
    logger.info("=== Testing Basic Database Connection ===")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info(" Basic connection successful")
            return True
    except Exception as e:
        logger.error(f" Basic connection failed: {e}")
        return False

def test_user_permissions():
    """Test database user permissions"""
    logger.info("=== Testing Database User Permissions ===")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # Get current user
            user_result = conn.execute(text("SELECT current_user, session_user")).fetchone()
            logger.info(f"Database user: {user_result[0]}, Session user: {user_result[1]}")
            
            # Check database name
            db_result = conn.execute(text("SELECT current_database()")).fetchone()
            logger.info(f"Current database: {db_result[0]}")
            
            # Test table access
            tables_result = conn.execute(text("""
                SELECT table_name, privilege_type 
                FROM information_schema.table_privileges 
                WHERE grantee = current_user 
                AND table_schema = 'public'
                LIMIT 10
            """)).fetchall()
            
            if tables_result:
                logger.info("User privileges:")
                for table, privilege in tables_result:
                    logger.info(f"  {table}: {privilege}")
            else:
                logger.warning("No table privileges found for current user")
            
            return True
    except Exception as e:
        logger.error(f" Permission check failed: {e}")
        return False

def test_table_operations():
    """Test actual table operations"""
    logger.info("=== Testing Table Operations ===")
    try:
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test if tables exist
        logger.info("Checking if tables exist...")
        tables = ['books', 'diseases', 'drugs', 'users']
        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
                logger.info(f" Table '{table}' exists with {result[0]} records")
            except Exception as e:
                logger.error(f" Table '{table}' error: {e}")
        
        # Test write operation with a simple test
        logger.info("Testing write operations...")
        try:
            # Try to create a test book
            test_book = models.Book(
                id=str(uuid.uuid4()),
                title="TEST_BOOK_DELETE_ME",
                description="Test book for diagnostics",
                category="test"
            )
            db.add(test_book)
            db.commit()
            logger.info(" Write operation successful")
            
            # Clean up test data
            db.delete(test_book)
            db.commit()
            logger.info(" Delete operation successful")
            
        except Exception as e:
            logger.error(f" Write operation failed: {e}")
            db.rollback()
            return False
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f" Table operations test failed: {e}")
        return False

def test_transaction_isolation():
    """Test transaction isolation and autocommit settings"""
    logger.info("=== Testing Transaction Settings ===")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # Check transaction isolation level
            isolation_result = conn.execute(text("SHOW transaction_isolation")).fetchone()
            logger.info(f"Transaction isolation level: {isolation_result[0]}")
            
            # Check autocommit status
            autocommit_result = conn.execute(text("SHOW autocommit")).fetchone()
            logger.info(f"Autocommit: {autocommit_result[0]}")
            
            return True
    except Exception as e:
        logger.error(f" Transaction settings check failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    logger.info(" Starting Database Diagnostics")
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    
    tests = [
        test_basic_connection,
        test_user_permissions,
        test_transaction_isolation,
        test_table_operations
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            logger.info("")
        except Exception as e:
            logger.error(f"Test {test.__name__} crashed: {e}")
            results.append(False)
    
    logger.info("=== Diagnostic Summary ===")
    if all(results):
        logger.info(" All tests passed! Database should be working correctly.")
    else:
        logger.error(" Some tests failed. Check the logs above for details.")
        logger.info("Common solutions:")
        logger.info("1. Ensure your database user has INSERT, UPDATE, DELETE permissions")
        logger.info("2. Check if your Railway PostgreSQL instance allows write operations")
        logger.info("3. Verify your DATABASE_URL is correct")
        logger.info("4. Make sure you're not using a read-only database connection")

if __name__ == "__main__":
    main()
