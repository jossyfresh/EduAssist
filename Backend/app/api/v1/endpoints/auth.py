from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.api import deps
from app.schemas.user import User, UserCreate, Token
from app.crud import crud_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

@router.post("/login", response_model=Token, responses={
    200: {
        "description": "Successfully logged in",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            }
        }
    },
    401: {"description": "Incorrect email or password"},
    400: {"description": "Inactive user"}
})
def login(
    db: Session = Depends(deps.get_db),
    login_data: LoginRequest = None
) -> Any:
    """Login to get access token.
    
    Example request body:
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    """
    user = crud_user.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=Token, responses={
    200: {
        "description": "Successfully registered",
        "content": {
            "application/json": {
                "example": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            }
        }
    },
    400: {
        "description": "Email already registered or Username already taken",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Email already registered"
                }
            }
        }
    }
})
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """Register a new user.
    
    Example request body:
    {
        "email": "user@example.com",
        "username": "johndoe",
        "password": "securepassword123",
        "full_name": "John Doe",
        "is_active": true,
        "is_superuser": false
    }
    """
    # Check if email is already registered
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Check if username is already taken
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # Create new user with all provided fields
    user_data = user_in.dict()
    user = crud_user.create(db, obj_in=UserCreate(**user_data))
    
    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.email, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    } 