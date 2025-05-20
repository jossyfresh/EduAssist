from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import ContentType

class LearningPathStep(Base):
    __tablename__ = "learning_path_steps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    content_type = Column(Enum(ContentType))
    content = Column(Text)
    order = Column(Integer)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    learning_path = relationship("LearningPath", back_populates="steps") 