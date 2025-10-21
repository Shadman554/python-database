# Veterinary Educational Platform API

## Overview
A production-ready FastAPI backend for veterinary education with comprehensive features including authentication, content management, push notifications, and more. This is version 3.0.0 of the API.

## Project Type
Backend API (FastAPI) - REST API with interactive documentation

## Current State
- ✅ Running successfully on Replit
- ✅ PostgreSQL database connected
- ✅ All dependencies installed
- ✅ API documentation available at `/docs`
- ✅ Deployment configured for Autoscale

## Recent Changes (2025-10-21)
- Fixed database URL configuration to use Replit's PostgreSQL instead of key-value store
- Added SQLAlchemy text construct to database queries for compatibility
- Updated CSP headers to allow Swagger UI resources
- Created .gitignore for Python project
- Configured workflow to run on port 5000
- Set up deployment with Gunicorn for production
- **Fixed Railway deployment crash**: Changed SECRET_KEY validation to auto-generate instead of crashing when missing in production
- Added RAILWAY_SETUP.md with deployment instructions

## Architecture

### Tech Stack
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn (development), Gunicorn (production)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Authentication**: JWT with refresh tokens, Google OAuth
- **Security**: bcrypt password hashing, rate limiting, CORS, security headers

### Project Structure
```
.
├── api/                    # API route modules
│   ├── auth.py            # Authentication endpoints
│   ├── dictionary.py      # Dictionary management
│   ├── diseases.py        # Disease database
│   ├── drugs.py           # Drug information
│   ├── books.py           # Educational resources
│   ├── users.py           # User management
│   ├── notifications.py   # Push notifications
│   └── ... (various test/slide modules)
├── main.py                # Application entry point
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic validation schemas
├── database.py            # Database configuration
├── auth.py                # Authentication logic
├── crud.py                # Database operations
├── config.py              # Settings management
├── logger.py              # Logging configuration
├── middleware.py          # Custom middleware
├── utils.py               # Utility functions
└── requirements.txt       # Python dependencies
```

### Key Features
1. **Authentication & Authorization**
   - JWT-based auth with refresh tokens
   - Google OAuth integration
   - Role-based access (Admin/User)

2. **Content Management**
   - Dictionary, diseases, drugs, books
   - Medical instruments & clinical notes
   - Lab test categories & slides
   - Normal ranges for lab values

3. **Security**
   - Rate limiting (60 req/min)
   - Security headers (CSP, HSTS, etc.)
   - Input validation
   - SQL injection protection

4. **Monitoring**
   - Comprehensive logging
   - Health check endpoint (`/health`)
   - Metrics endpoint (`/metrics`)
   - Request/response tracking

## Environment Variables
The application uses environment variables for configuration:
- `ENVIRONMENT`: development/production
- `DATABASE_URL`: PostgreSQL connection (auto-configured on Replit)
- `SECRET_KEY`: JWT secret (auto-generated in dev)
- `CORS_ORIGINS`: Allowed CORS origins
- `RATE_LIMIT_REQUESTS`: Rate limit threshold
- Google OAuth credentials (optional)
- OneSignal push notification keys (optional)

## Deployment
- **Type**: Autoscale (stateless API)
- **Command**: Gunicorn with 4 workers
- **Port**: 5000
- **Worker Class**: uvicorn.workers.UvicornWorker

## API Documentation
- **Swagger UI**: https://[repl-url]/docs
- **ReDoc**: https://[repl-url]/redoc
- **OpenAPI Spec**: https://[repl-url]/openapi.json

## Database
Uses Replit's PostgreSQL database. Tables are auto-created on startup using SQLAlchemy models.

## Notes
- API documentation only available in development mode
- CORS is currently set to allow all origins (should be restricted in production)
- Using auto-generated SECRET_KEY in development
- Database connection pooling configured for PostgreSQL
