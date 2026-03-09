from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config import settings
import models
import uuid
import secrets
from logger import auth_logger, log_security_event

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    """Verify password against hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        auth_logger.error(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password):
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token
    
    Args:
        data: Payload data to encode
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    auth_logger.debug(f"Created access token for user: {data.get('sub')}")
    return encoded_jwt

def create_refresh_token(db: Session, user_id: str) -> str:
    """
    Create and store refresh token
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        Refresh token string
    """
    # Generate secure random token
    token = secrets.token_urlsafe(64)
    
    # Calculate expiration
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Store in database
    refresh_token = models.RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    
    db.add(refresh_token)
    db.commit()
    
    auth_logger.info(f"Created refresh token for user: {user_id}")
    return token

def verify_refresh_token(db: Session, token: str) -> Optional[models.User]:
    """
    Verify refresh token and return associated user
    
    Args:
        db: Database session
        token: Refresh token string
        
    Returns:
        User object if valid, None otherwise
    """
    refresh_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token,
        models.RefreshToken.revoked == False
    ).first()
    
    if not refresh_token:
        log_security_event("Invalid refresh token used", {"token_prefix": token[:10]})
        return None
    
    # Check expiration
    if refresh_token.expires_at < datetime.utcnow():
        log_security_event("Expired refresh token used", {"user_id": refresh_token.user_id})
        return None
    
    # Get user
    user = db.query(models.User).filter(models.User.id == refresh_token.user_id).first()
    
    if user:
        auth_logger.debug(f"Refresh token verified for user: {user.username}")
    
    return user

def revoke_refresh_token(db: Session, token: str):
    """Revoke a refresh token"""
    refresh_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token
    ).first()
    
    if refresh_token:
        refresh_token.revoked = True
        db.commit()
        auth_logger.info(f"Revoked refresh token for user: {refresh_token.user_id}")

def revoke_all_user_tokens(db: Session, user_id: str):
    """Revoke all refresh tokens for a user"""
    db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id,
        models.RefreshToken.revoked == False
    ).update({"revoked": True})
    db.commit()
    auth_logger.info(f"Revoked all tokens for user: {user_id}")

def verify_token(credentials: HTTPAuthorizationCredentials, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(credentials: HTTPAuthorizationCredentials, db: Session):
    return verify_token(credentials, db)

def get_current_admin_user(credentials: HTTPAuthorizationCredentials, db: Session):
    user = verify_token(credentials, db)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user
