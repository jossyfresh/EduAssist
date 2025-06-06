from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    created_quizzes = relationship("Quiz", back_populates="creator")
    created_flashcards = relationship("Flashcard", back_populates="creator")
    created_exams = relationship("Exam", back_populates="creator")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    exam_attempts = relationship("ExamAttempt", back_populates="user")
    youtube_contents = relationship("YouTubeContent", back_populates="user")
    youtube_chat_messages = relationship("YouTubeChatMessage", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>" 