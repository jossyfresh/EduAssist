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

# Quiz schemas
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionCreate]
    passing_score: float
    time_limit: Optional[int] = None  # in minutes

class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    title: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    passing_score: Optional[float] = None

class Quiz(QuizBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QuizAttempt(BaseModel):
    quiz_id: UUID4
    user_id: UUID4
    score: float
    answers: Dict[str, str]  # question_id: answer
    started_at: datetime
    completed_at: datetime

    class Config:
        from_attributes = True

# Flashcard schemas
class FlashcardBase(BaseModel):
    front: str
    back: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(FlashcardBase):
    front: Optional[str] = None
    back: Optional[str] = None

class Flashcard(FlashcardBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Exam schemas
class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[QuestionCreate]
    passing_score: float
    time_limit: Optional[int] = None  # in minutes
    is_proctored: bool = False

class ExamCreate(ExamBase):
    pass

class ExamUpdate(ExamBase):
    title: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    passing_score: Optional[float] = None

class Exam(ExamBase):
    id: UUID4
    created_by: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExamAttempt(BaseModel):
    exam_id: UUID4
    user_id: UUID4
    score: float
    answers: Dict[str, str]  # question_id: answer
    started_at: datetime
    completed_at: datetime
    is_proctored: bool = False

    class Config:
        from_attributes = True 