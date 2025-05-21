from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import logging

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from app.core.security_scheme import security as api_security

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(api_security)
) -> User:
    try:
        token = credentials.credentials
        logger.debug(f"Received token: {token}")
        
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            logger.debug(f"Decoded payload: {payload}")
        except jwt.JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        email: str = payload.get("sub")
        if email is None:
            logger.error("No email in token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug(f"Looking up user with email: {email}")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.error(f"No user found for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.debug(f"Found user: {user.email}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        logger.error(f"Inactive user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        logger.error(f"Non-superuser access attempt: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user 