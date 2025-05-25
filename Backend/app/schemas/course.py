from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    pass

class CourseCreate(BaseModel):
    prompt: str

class CourseUpdate(BaseModel):
    title: str = None
    sub_title: str = None
    description: str = None

class Course(CourseBase):
    id: str
    title: str
    sub_title: str = None
    description: str = None
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
