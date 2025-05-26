from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserProgressBase(BaseModel):
    completed: bool = False
    completed_at: Optional[datetime] = None

class UserProgressCreate(UserProgressBase):
    learning_path_id: str
    step_id: str

class UserProgressUpdate(UserProgressBase):
    pass

class UserProgressInDB(UserProgressBase):
    id: str
    user_id: str
    learning_path_id: str
    step_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 