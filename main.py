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
    auth as auth_api, users, books, diseases, drugs, dictionary, 
    notifications, normal_ranges, 
    app_links, about, instruments, notes, urine_slides, stool_slides, other_slides, leaderboard
)
from auth import verify_token

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Veterinary Educational Platform API",
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
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
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