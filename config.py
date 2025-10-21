import os
from dotenv import load_dotenv
from typing import List
import secrets

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

class Settings:
    """Application settings with validation"""
    
    def __init__(self):
        # Environment
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
        self.DEBUG = self.ENVIRONMENT == 'development'
        
        # Database - Use Railway public URL when available, fallback to Replit or SQLite
        self.DATABASE_URL = os.getenv(
            'DATABASE_PUBLIC_URL',
            os.getenv('REPLIT_DB_URL', os.getenv('DATABASE_URL', 'sqlite:///./production.db'))
        )
        
        # JWT - Validate SECRET_KEY in production
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        if not self.SECRET_KEY:
            if self.ENVIRONMENT == 'production':
                raise ValueError("SECRET_KEY must be set in production environment!")
            else:
                # Generate a random key for development
                self.SECRET_KEY = secrets.token_urlsafe(32)
                print(f"⚠️  WARNING: Using auto-generated SECRET_KEY for development")
        
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
        self.REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '7'))
        
        # CORS - Validate origins in production
        cors_origins = os.getenv('CORS_ORIGINS', '')
        if self.ENVIRONMENT == 'production' and not cors_origins:
            print("⚠️  WARNING: CORS_ORIGINS not set in production. Using wildcard (*).")
            self.CORS_ORIGINS = ["*"]
        elif cors_origins:
            self.CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
        else:
            self.CORS_ORIGINS = ["*"]
        
        # File upload
        self.UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        self.ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        # Pagination
        self.DEFAULT_PAGE_SIZE = 20
        self.MAX_PAGE_SIZE = 100
        
        # Rate limiting
        self.RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '60'))
        self.RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds
        
        # Google OAuth
        self.GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
        self.GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
        self.GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID', '')
        
        # OneSignal
        self.ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID', '')
        self.ONESIGNAL_REST_API_KEY = os.getenv('ONESIGNAL_REST_API_KEY', '')
        
        # Database connection pool
        self.DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
        self.DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '10'))
        self.DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        self.DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', '3600'))
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT == 'development'

settings = Settings()