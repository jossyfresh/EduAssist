from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    sub_title: Optional[str] = None
    description: Optional[str] = None

class CourseCreate(BaseModel):
    prompt: str
    title: Optional[str] = None
    sub_title: Optional[str] = None
    description: Optional[str] = None

class CourseUpdate(CourseBase):
    title: Optional[str] = None

class Course(CourseBase):
    id: str
    creator_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
