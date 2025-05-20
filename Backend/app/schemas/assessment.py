from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, UUID4, Field

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(QuestionBase):
    question: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None

class QuestionInDB(QuestionBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionCreate]
    passing_score: float
    time_limit: Optional[int] = None  # in minutes

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentUpdate(AssessmentBase):
    title: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    passing_score: Optional[float] = None

class AssessmentInDB(AssessmentBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    assessment_id: UUID4
    user_id: UUID4
    score: float
    answers: Dict[str, str]  # question_id: answer
    started_at: datetime
    completed_at: datetime

    class Config:
        from_attributes = True 