import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

class Settings:
    # Database - Use Railway public URL when available, fallback to Replit or SQLite
    DATABASE_URL = os.getenv('DATABASE_PUBLIC_URL', os.getenv('REPLIT_DB_URL', os.getenv('DATABASE_URL', 'sqlite:///./production.db')))

    # JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'production-secret-key-change-this-in-production-2024')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # File upload
    UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.gif'}

    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # Rate limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 3600  # 1 hour

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID', '')

settings = Settings()