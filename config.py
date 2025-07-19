
import os

class Settings:
    def __init__(self):
        # Try multiple environment variable names for database URL
        self.DATABASE_URL = self._get_database_url()

        # JWT Configuration
        self.SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

        # File upload
        self.UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
        self.MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        self.ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.gif'}
        
        # Pagination
        self.DEFAULT_PAGE_SIZE = 20
        self.MAX_PAGE_SIZE = 100
        
        # Rate limiting
        self.RATE_LIMIT_REQUESTS = 100
        self.RATE_LIMIT_WINDOW = 3600  # 1 hour

    def _get_database_url(self) -> str:
        """Get database URL from various possible environment variables"""
        # Try different possible environment variable names
        url_sources = [
            'DATABASE_URL',
            'RAILWAY_DATABASE_URL', 
            'POSTGRES_URL',
            'DB_URL'
        ]

        for source in url_sources:
            url = os.getenv(source)
            if url and url.strip():
                print(f"✅ Found database URL from {source}")
                return url

        # Fallback to local SQLite
        fallback_url = 'sqlite:///./local_dev.db'
        print(f"⚠️ No database URL found in environment, using fallback: {fallback_url}")
        return fallback_url

settings = Settings()
