from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4
from app.models.enums import ProgressStatus

class UserProgressBase(BaseModel):
    status: ProgressStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class UserProgressCreate(UserProgressBase):
    learning_path_id: UUID4
    step_id: UUID4

class UserProgressUpdate(UserProgressBase):
    status: Optional[ProgressStatus] = None

class UserProgressInDB(UserProgressBase):
    id: UUID4
    user_id: UUID4
    learning_path_id: UUID4
    step_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 