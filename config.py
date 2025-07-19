
import os
from python_decouple import config

class Settings:
    def __init__(self):
        # Try multiple environment variable names for database URL
        self.DATABASE_URL = self._get_database_url()

        # JWT Configuration
        self.SECRET_KEY: str = config('SECRET_KEY', default='your-secret-key-here-change-in-production')
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

        # File upload
        self.UPLOAD_DIR = config('UPLOAD_DIR', default='uploads')
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
            'DATABASE_PUBLIC_URL',  # Railway public URL first
            'DATABASE_URL',
            'RAILWAY_DATABASE_URL', 
            'POSTGRES_URL',
            'DB_URL'
        ]

        for source in url_sources:
            url = config(source, default=None)
            if url and url.strip():
                # Check if it's an internal Railway URL and warn
                if 'railway.internal' in url:
                    print(f"⚠️ Found internal Railway URL from {source}, this won't work externally")
                    continue
                print(f"✅ Found database URL from {source}")
                return url

        # If no public URL found, construct one from Railway environment variables
        pg_user = config('PGUSER', default=None)
        pg_password = config('PGPASSWORD', default=None) 
        pg_database = config('PGDATABASE', default=None)
        railway_tcp_domain = config('RAILWAY_TCP_PROXY_DOMAIN', default=None)
        railway_tcp_port = config('RAILWAY_TCP_PROXY_PORT', default=None)

        if all([pg_user, pg_password, pg_database, railway_tcp_domain, railway_tcp_port]):
            constructed_url = f"postgresql://{pg_user}:{pg_password}@{railway_tcp_domain}:{railway_tcp_port}/{pg_database}"
            print(f"✅ Constructed Railway public database URL")
            return constructed_url

        # Fallback to local SQLite
        fallback_url = 'sqlite:///./local_dev.db'
        print(f"⚠️ No database URL found in environment, using fallback: {fallback_url}")
        return fallback_url

settings = Settings()
