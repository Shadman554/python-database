import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='.env')

class Settings:
    # Database - Use Railway public URL format
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./local_dev.db')
    
    # For Railway, ensure we're using the public URL format
    if DATABASE_URL and 'railway.internal' in DATABASE_URL:
        # Convert internal URL to public format
        DATABASE_URL = DATABASE_URL.replace(
            'postgres.railway.internal:5432',
            'roundhouse.proxy.rlwy.net:13307'  # Standard Railway proxy port
        )
    
    # JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
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

settings = Settings()
