from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepassword123",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False
            }
        }

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

class User(UserInDBBase):
    class Config:
        orm_mode = True
        from_attributes = True

class UserInDB(UserInDBBase):
    hashed_password: str 