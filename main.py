from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os

from database import engine, get_db
from models import Base
from api import (
    auth as auth_api, users, books, diseases, drugs, dictionary, questions, 
    notifications, staff, normal_ranges, 
    app_links, about, instruments, notes, urine_slides, stool_slides, other_slides, leaderboard
)
from auth import verify_token

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Veterinary Educational Platform API",
    description="""
    A comprehensive API for veterinary education with multilingual content management.

    ## Features
    - **Authentication**: JWT-based user authentication with role-based access
    - **Content Management**: CRUD operations for educational content
    - **Search by Name**: All entities can be accessed by name/title in addition to ID
    - **Multilingual Support**: Content in English, Kurdish, and Arabic
    - **File Management**: Upload and serve educational resources
    - **User Interaction**: Questions, notifications, and points system

    ## Available Endpoints
    - **Books**: Access by ID or title (`/api/books/by-title/{title}`)
    - **Diseases**: Access by ID or name (`/api/diseases/by-name/{name}`)
    - **Drugs**: Access by ID or name (`/api/drugs/by-name/{name}`)
    - **Dictionary**: Access by ID or word (`/api/dictionary/by-name/{word}`)
    - **Staff**: Access by ID or name (`/api/staff/by-name/{name}`)
    - **Tutorial Videos**: Access by ID or title (`/api/tutorial-videos/by-title/{title}`)
    - **Normal Ranges**: Access by ID or name (`/api/normal-ranges/by-name/{name}`)
    - **Questions**: Access by ID or user (`/api/questions/by-user/{user_name}`)
    - **Users**: User management and authentication
    - **Notifications**: System notifications
    - **App Links**: Mobile app download links
    - **About**: About page content

    ## Authentication
    Multiple authentication methods are supported:
    - **Standard Login**: Use `/api/auth/login` with username/password
    - **Google OAuth**: Use `/api/auth/google-login` with a Google OAuth token
    - **Registration**: Use `/api/auth/register` or `/api/auth/google-register`

    After authentication, include the JWT token in the Authorization header as `Bearer <token>`.
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth_api.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(diseases.router, prefix="/api/diseases", tags=["Diseases"])
app.include_router(drugs.router, prefix="/api/drugs", tags=["Drugs"])
app.include_router(dictionary.router, prefix="/api/dictionary", tags=["Dictionary"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(staff.router, prefix="/api/staff", tags=["Staff"])
app.include_router(normal_ranges.router, prefix="/api/normal-ranges", tags=["Normal Ranges"])
app.include_router(app_links.router, prefix="/api/app-links", tags=["App Links"])
app.include_router(about.router, prefix="/api/about", tags=["About"])
app.include_router(instruments.router, prefix="/api/instruments", tags=["instruments"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(urine_slides.router, prefix="/api/urine-slides", tags=["urine-slides"])
app.include_router(stool_slides.router, prefix="/api/stool-slides", tags=["stool-slides"])
app.include_router(other_slides.router, prefix="/api/other-slides", tags=["other-slides"])
app.include_router(about.router, prefix="/api/about", tags=["about"])
app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["leaderboard"])

@app.get("/")
async def root():
    return {"message": "Veterinary Educational Platform API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )