from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, UUID4

class ProgressBase(BaseModel):
    completed: bool = False
    completed_at: Optional[datetime] = None

class ProgressCreate(ProgressBase):
    learning_path_id: str
    step_id: str

class ProgressUpdate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: str
    user_id: str
    learning_path_id: str
    step_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssessmentProgressBase(BaseModel):
    score: Optional[float] = None
    attempts: int = 0
    last_attempt_at: Optional[datetime] = None
    best_score: Optional[float] = None

class AssessmentProgressCreate(AssessmentProgressBase):
    course_id: str
    assessment_type: str
    assessment_id: str

class AssessmentProgressUpdate(AssessmentProgressBase):
    pass

class AssessmentProgress(AssessmentProgressBase):
    id: str
    user_id: str
    course_id: str
    assessment_type: str
    assessment_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseProgressBase(BaseModel):
    overall_score: float = 0.0
    completed_assessments: int = 0
    total_assessments: int = 0
    last_activity_at: Optional[datetime] = None

class CourseProgressCreate(CourseProgressBase):
    course_id: str

class CourseProgressUpdate(CourseProgressBase):
    pass

class CourseProgress(CourseProgressBase):
    id: str
    user_id: str
    course_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProgressAnalytics(BaseModel):
    total_courses: int
    completed_courses: int
    average_score: float
    total_assessments: int
    completed_assessments: int
    recent_activity: List[datetime]
    course_progress: List[CourseProgress]
    assessment_progress: List[AssessmentProgress]

class Achievement(BaseModel):
    id: UUID4
    user_id: UUID4
    title: str
    description: Optional[str] = None
    achieved_at: datetime

    class Config:
        from_attributes = True 