from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.db.session import engine
from app.models.user import User

def init_db() -> None:
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine) 