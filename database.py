import os
from sqlalchemy import create_engine, event, exc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool
from dotenv import load_dotenv
from config import settings
from logger import db_logger
import time

load_dotenv()

# Use Railway public URL when available, fallback to Replit or SQLite
DATABASE_URL = settings.DATABASE_URL

# Configure engine with proper settings for production
engine_kwargs = {
    "pool_pre_ping": True,  # Verify connections before using
    "echo": settings.DEBUG,  # Log SQL in debug mode
}

if DATABASE_URL.startswith('sqlite'):
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
    })
    db_logger.info("Using SQLite database")
elif DATABASE_URL.startswith('postgresql'):
    engine_kwargs.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
    })
    db_logger.info("Using PostgreSQL database with connection pooling")
else:
    db_logger.info(f"Using database: {DATABASE_URL.split(':')[0]}")

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Add connection pool event listeners for monitoring
@event.listens_for(Pool, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Log new database connections"""
    db_logger.debug("New database connection established")

@event.listens_for(Pool, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Log connection checkout from pool"""
    db_logger.debug("Connection checked out from pool")

@event.listens_for(Pool, "checkin")
def receive_checkin(dbapi_conn, connection_record):
    """Log connection return to pool"""
    db_logger.debug("Connection returned to pool")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Database session dependency with automatic cleanup
    Includes retry logic for transient failures
    """
    db = SessionLocal()
    try:
        yield db
    except exc.DBAPIError as e:
        db_logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def check_db_connection(max_retries: int = 3, retry_delay: int = 2) -> bool:
    """
    Check database connection health with retry logic
    
    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        True if connection successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            # Try to connect and execute a simple query
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            db_logger.info("Database connection successful")
            return True
        except Exception as e:
            db_logger.warning(
                f"Database connection attempt {attempt + 1}/{max_retries} failed: {str(e)}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    db_logger.error("Failed to connect to database after all retries")
    return False

def get_db_info() -> dict:
    """Get database connection information"""
    return {
        "url": DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL.split(':')[0],
        "dialect": engine.dialect.name,
        "pool_size": getattr(engine.pool, 'size', lambda: 'N/A')(),
        "pool_checked_out": getattr(engine.pool, 'checkedout', lambda: 'N/A')(),
        "pool_overflow": getattr(engine.pool, 'overflow', lambda: 'N/A')(),
    }