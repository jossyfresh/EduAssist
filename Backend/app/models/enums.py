from enum import Enum

class ContentType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    QUIZ = "quiz"
    EXERCISE = "exercise"

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed" 