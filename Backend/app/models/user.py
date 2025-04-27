from sqlalchemy import Column, String, UUID
from app.models.base import Base, TimestampMixin
import uuid

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    avatar_url = Column(String)
    hashed_password = Column(String, nullable=False)
    
    def __repr__(self):
        return f"<User {self.email}>" 