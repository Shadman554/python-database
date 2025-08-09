#!/usr/bin/env python3
"""
Railway Deployment Script for Veterinary Educational Platform API
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if Railway CLI is installed"""
    try:
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        print("✓ Railway CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Railway CLI is not installed")
        print("Please install it from: https://docs.railway.app/cli/installation")
        return False

def create_railway_project():
    """Create a new Railway project"""
    print("\n=== Creating Railway Project ===")
    print("1. Run: railway login")
    print("2. Run: railway new")
    print("3. Select your project name")
    print("4. Link this directory to the project")

def setup_database():
    """Instructions for setting up PostgreSQL database"""
    print("\n=== Setting up PostgreSQL Database ===")
    print("1. In Railway dashboard, click 'Add Database'")
    print("2. Select 'PostgreSQL'")
    print("3. Wait for database to be created")
    print("4. Go to Variables tab and copy the DATABASE_URL")

def deploy_application():
    """Deploy the FastAPI application"""
    print("\n=== Deploying Application ===")
    print("1. Set environment variables in Railway:")
    print("   - DATABASE_URL (from PostgreSQL service)")
    print("   - SECRET_KEY (generate a secure key)")
    print("   - PORT (Railway will set this automatically)")
    print("")
    print("2. Run: railway up")
    print("3. Your API will be available at the generated Railway URL")

def import_data_to_railway():
    """Instructions for importing data to Railway database"""
    print("\n=== Importing Data to Railway Database ===")
    print("1. Update DATABASE_URL in your environment")
    print("2. Run: python import_data.py")
    print("3. This will create tables and import all veterinary data")

def main():
    print("=== Railway Deployment Guide ===")
    print("This script will guide you through deploying your FastAPI app to Railway")
    
    if not check_dependencies():
        return
    
    create_railway_project()
    setup_database()
    deploy_application()
    import_data_to_railway()
    
    print("\n=== Final Steps ===")
    print("1. Test your API at: https://your-app-name.railway.app")
    print("2. API documentation: https://your-app-name.railway.app/docs")
    print("3. Your database is now hosted on Railway's infrastructure")

if __name__ == "__main__":
    main()