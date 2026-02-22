from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
import models
import schemas
import crud
from database import get_db
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from config import settings
import google.auth.transport.requests
import google.oauth2.id_token
import uuid

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        db_user = crud.get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        db_user = crud.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        db_user = crud.create_user(db, user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access and refresh tokens"""
    try:
        user = authenticate_user(db, user_credentials.username, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Create refresh token
        from auth import create_refresh_token
        refresh_token = create_refresh_token(db, user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to login: {str(e)}")

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        current_user = get_current_user(credentials, db)
        
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user information: {str(e)}")

@router.post("/refresh", response_model=schemas.Token)
async def refresh_token_endpoint(
    refresh_request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        from auth import verify_refresh_token, create_refresh_token
        
        # Verify refresh token and get user
        user = verify_refresh_token(db, refresh_request.refresh_token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Optionally create new refresh token (rotation)
        new_refresh_token = create_refresh_token(db, user.id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh token: {str(e)}")

@router.post("/logout")
async def logout(
    refresh_request: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Logout user and revoke refresh token"""
    try:
        from auth import revoke_refresh_token
        
        revoke_refresh_token(db, refresh_request.refresh_token)
        
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to logout: {str(e)}")

@router.post("/google-login", response_model=schemas.Token)
async def google_login(request: Request, db: Session = Depends(get_db)):
    """Authenticate user with Google OAuth token"""
    try:
        body = await request.json()
        google_token = body.get("token")

        if not google_token:
            raise HTTPException(status_code=400, detail="Google token is required")

        # Verify the Google token
        try:
            if not settings.GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=500, 
                    detail="Google OAuth is not configured on the server. Please contact the administrator."
                )
            
            idinfo = google.oauth2.id_token.verify_oauth2_token(
                google_token, 
                google.auth.transport.requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # Extract user information from Google token
            google_user_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            given_name = idinfo.get('given_name', '')
            family_name = idinfo.get('family_name', '')
            photo_url = idinfo.get('picture', '')

        except ValueError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")

        # Check if user exists
        db_user = crud.get_user_by_email(db, email)

        if not db_user:
            # Create new user with Google authentication
            username = email.split('@')[0] + '_' + str(uuid.uuid4())[:8]

            # Create a random password (bcrypt has 72 byte limit, so keep it short)
            # Google users don't use this password directly
            random_password = str(uuid.uuid4())[:32]

            user_data = schemas.UserCreate(
                username=username,
                email=email,
                password=random_password,
                photo_url=photo_url
            )

            db_user = crud.create_user(db, user_data)
        else:
            # Update photo_url if Google provides one and it's different
            if photo_url and db_user.photo_url != photo_url:
                db_user.photo_url = photo_url
                db.commit()
                db.refresh(db_user)

        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to authenticate with Google: {str(e)}")

@router.post("/google-register", response_model=schemas.User)
async def google_register(request: Request, db: Session = Depends(get_db)):
    """Register a new user with Google OAuth"""
    try:
        body = await request.json()
        google_token = body.get("token")

        if not google_token:
            raise HTTPException(status_code=400, detail="Google token is required")

        # Verify the Google token
        try:
            if not settings.GOOGLE_CLIENT_ID:
                raise HTTPException(
                    status_code=500, 
                    detail="Google OAuth is not configured on the server. Please contact the administrator."
                )
            
            idinfo = google.oauth2.id_token.verify_oauth2_token(
                google_token, 
                google.auth.transport.requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # Extract user information from Google token
            google_user_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            photo_url = idinfo.get('picture', '')

        except ValueError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")

        # Check if user already exists
        db_user = crud.get_user_by_email(db, email)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")

        # Create username from email and add random suffix to ensure uniqueness
        base_username = email.split('@')[0]
        username = base_username
        counter = 1

        # Ensure username uniqueness
        while crud.get_user_by_username(db, username):
            username = f"{base_username}_{counter}"
            counter += 1

        # Create a random password (bcrypt has 72 byte limit, so keep it short)
        # Google users don't use this password directly
        random_password = str(uuid.uuid4())[:32]

        user_data = schemas.UserCreate(
            username=username,
            email=email,
            password=random_password,
            photo_url=photo_url
        )

        db_user = crud.create_user(db, user_data)
        return db_user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register with Google: {str(e)}")

@router.delete("/delete-account")
async def delete_account(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Delete current user's account"""
    try:
        current_user = get_current_user(credentials, db)
        
        # Delete the user's account
        crud.delete_item(db, current_user)
        
        return {"message": "Account deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")

@router.post("/update_points")
async def update_points(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Update user points"""
    try:
        current_user = get_current_user(credentials, db)
        body = await request.json()
        points = body.get("points", 0)
        
        if not isinstance(points, int):
            raise HTTPException(status_code=400, detail="Points must be an integer")
        
        updated_user = crud.update_user_points(db, current_user.id, points)
        return {
            "message": f"Updated points by {points}",
            "total_points": updated_user.total_points,
            "today_points": updated_user.today_points
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update points: {str(e)}")

@router.post("/add-points")
async def add_points(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Add points to user"""
    try:
        current_user = get_current_user(credentials, db)
        body = await request.json()
        points = body.get("points", 0)
        
        if not isinstance(points, int) or points < 0:
            raise HTTPException(status_code=400, detail="Points must be a positive integer")
        
        updated_user = crud.update_user_points(db, current_user.id, points)
        return {
            "message": f"Added {points} points",
            "total_points": updated_user.total_points,
            "today_points": updated_user.today_points
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add points: {str(e)}")