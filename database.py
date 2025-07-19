from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate database URL before using it
if not settings.DATABASE_URL or settings.DATABASE_URL.strip() == "":
    logger.error("❌ Database URL is empty or not set!")
    raise ValueError("DATABASE_URL environment variable is required")

logger.info(f"Connecting to database: {settings.DATABASE_URL[:50]}...")

try:
    # Additional connection parameters for different database types
    connect_args = {}
    if settings.DATABASE_URL.startswith('sqlite'):
        connect_args = {"check_same_thread": False}
    
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,  # Set to True for SQL debugging
        connect_args=connect_args
    )
    logger.info("✅ Database engine created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create database engine: {e}")
    logger.error(f"Database URL: {settings.DATABASE_URL}")
    raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session created")
        yield db
        logger.info("Database session completed successfully")
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise e
    finally:
        db.close()
        logger.info("Database session closed")
