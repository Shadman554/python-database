# Veterinary Educational Platform API

## Overview

This is a comprehensive REST API for a veterinary educational platform that provides multilingual content management for veterinary education. The system serves as a backend for a mobile application that helps veterinary students and professionals access educational resources including books, diseases information, drug details, dictionary terms, and tutorial videos.

## User Preferences

Preferred communication style: Simple, everyday language.
User wants to deploy to Railway hosting platform with PostgreSQL database.

## System Architecture

### Backend Architecture
- **Framework**: FastAPI (Python) - A modern, fast web framework for building APIs
- **Database**: PostgreSQL with SQLAlchemy ORM for database operations
- **Authentication**: JWT (JSON Web Tokens) with bcrypt password hashing
- **API Design**: RESTful architecture with modular router structure

### Data Storage Solutions
- **Primary Database**: PostgreSQL for structured data storage
- **File Storage**: Local file system with configurable upload directory
- **Migration Management**: Alembic for database schema versioning

### Authentication and Authorization
- **JWT Authentication**: Token-based authentication with configurable expiration
- **Role-Based Access**: User and admin roles with different permissions
- **Password Security**: bcrypt hashing for secure password storage
- **API Security**: HTTP Bearer token authentication

## Key Components

### Core Models
1. **User Management**: User accounts with points system and admin privileges
2. **Educational Content**: Books, diseases, drugs, dictionary words
3. **Interactive Features**: Questions, notifications, tutorial videos
4. **Reference Data**: Normal ranges, staff information, app links, about page

### API Modules
- **Authentication**: User registration, login, token management
- **Content Management**: CRUD operations for all educational content
- **File Management**: Upload and serve educational resources
- **User Interaction**: Questions, notifications, points tracking

### Database Schema
- UUID-based primary keys for all entities
- Multilingual support (English, Kurdish, Arabic)
- Timestamp tracking for created/updated records
- Flexible JSON fields for additional metadata

## Data Flow

1. **User Authentication**: Users authenticate via JWT tokens
2. **Content Access**: Authenticated users can access educational content
3. **Admin Operations**: Admin users can create, update, and delete content
4. **File Operations**: Support for PDF, image uploads with validation
5. **Search & Filter**: Full-text search capabilities across content
6. **Pagination**: Consistent pagination across all list endpoints

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework and API documentation
- **SQLAlchemy**: Database ORM and query builder
- **Alembic**: Database migration management
- **python-jose**: JWT token handling
- **passlib**: Password hashing and verification
- **python-decouple**: Environment configuration management

### Data Import
- **Firebase Migration**: Import scripts for migrating data from Firebase
- **JSON Data Processing**: Utilities for processing exported Firebase data

## Deployment Strategy

### Railway Platform Deployment
- **Target Platform**: Railway.app for PostgreSQL database hosting
- **Database**: Railway PostgreSQL service with automatic provisioning
- **Environment Variables**: DATABASE_URL, SECRET_KEY, PORT configured via Railway
- **Deployment Files**: railway.json, deploy_railway.py, migrate_to_railway.py

### Configuration Management
- Environment-based configuration using os.getenv()
- Configurable database URLs from Railway PostgreSQL service
- Separate settings for development and production
- Railway-specific environment variable handling

### Database Management
- Automatic table creation on startup
- Database connection pooling with health checks
- Railway PostgreSQL database integration
- Data migration scripts for Railway deployment

### File Management
- Configurable upload directory
- File size and type validation
- Local file serving capabilities

### API Documentation
- Auto-generated OpenAPI documentation
- Interactive API explorer at /docs endpoint
- RESTful API design with consistent response formats

The system is designed to be scalable and maintainable, with clear separation of concerns between authentication, business logic, and data access layers. The modular structure allows for easy extension and modification of individual components.