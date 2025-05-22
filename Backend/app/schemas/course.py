from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
