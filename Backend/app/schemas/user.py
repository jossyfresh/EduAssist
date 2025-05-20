from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: str
    username: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str 