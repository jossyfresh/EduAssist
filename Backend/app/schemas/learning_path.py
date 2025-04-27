from pydantic import BaseModel
from typing import Optional

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None

class LearningPathCreate(LearningPathBase):
    pass

class LearningPathUpdate(LearningPathBase):
    title: Optional[str] = None

class LearningPath(LearningPathBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True 