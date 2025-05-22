from datetime import datetime
from typing import Dict, Optional, List
from uuid import UUID
from pydantic import BaseModel, Field

class LearningPathStepBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int
    content_id: Optional[UUID] = None
    learning_path_id: UUID

class LearningPathStepCreate(LearningPathStepBase):
    pass

class LearningPathStepUpdate(LearningPathStepBase):
    title: Optional[str] = None
    order: Optional[int] = None
    learning_path_id: Optional[UUID] = None

class LearningPathStepInDB(LearningPathStepBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LearningPathStep(LearningPathStepInDB):
    pass

class LearningPathStepReorder(BaseModel):
    step_orders: List[Dict[str, int]] 