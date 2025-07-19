import os
from decouple import config

class Settings:
    def __init__(self):
        # Try multiple environment variable names for database URL
        self.DATABASE_URL = self._get_database_url()

        # JWT Configuration
        self.SECRET_KEY: str = config('SECRET_KEY', default='your-secret-key-here-change-in-production')
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
            url = config(source, default=None)
            if url and url.strip():
                print(f"✅ Found database URL from {source}")
                return url

        # Fallback to local SQLite
        fallback_url = 'sqlite:///./local_dev.db'
        print(f"⚠️ No database URL found in environment, using fallback: {fallback_url}")
        return fallback_url

settings = Settings()