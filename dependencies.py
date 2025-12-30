from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import SessionLocal, User
from utils.security import decode_access_token
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

# Authentication mode: "production" (JWT required) or "development" (optional)
AUTH_MODE = os.getenv("AUTH_MODE", "development")
# Development mode default user
DEV_USER_ID = 1
DEV_USERNAME = "test_user"

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_dev_user(db: Session) -> User:
    """Get or create a test user for development"""
    user = db.query(User).filter(User.id == DEV_USER_ID).first()
    if not user:
        from utils.security import get_password_hash
        user = User(
            id=DEV_USER_ID,
            username=DEV_USERNAME,
            hashed_password=get_password_hash("dev_password")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Development user created: {DEV_USERNAME}")
    return user

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token or development mode.
    
    In development mode: Returns default test user
    In production mode: Requires valid JWT token
    """
    # Development mode - return default user without token validation
    if AUTH_MODE == "development":
        logger.debug("Development mode: Using default test user")
        return get_or_create_dev_user(db)
    
    # Production mode - require valid token
    if not credentials:
        logger.warning("Missing authentication credentials in production mode")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    
    # Fetch user from database
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.warning(f"Token valid but user not found: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

def get_current_user_id(
    current_user: User = Depends(get_current_user)
) -> int:
    """Convenience function to get just the user_id"""
    return current_user.id