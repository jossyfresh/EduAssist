import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from uuid import UUID, uuid4
from datetime import datetime
from app.core.security import create_access_token
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathStepCreate,
    UserProgressCreate,
    ProgressStatus
)
from app.schemas.content import ContentCreate
from app.models.enums import ContentType
from app.db.session import SessionLocal, engine
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

# Set test environment variables
os.environ["TESTING"] = "True"
os.environ["SQLITE_URL"] = "sqlite:///Backend/test.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["OPENAI_API_KEY"] = "test-openai-key"
os.environ["GEMINI_API_KEY"] = "test-gemini-key"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # Create test database tables
    from app.db.base_class import Base
    Base.metadata.drop_all(bind=engine)  # Drop all tables first
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up test database
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client() -> TestClient:
    """Test client fixture."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function", autouse=True)
def setup_test_environment(db: Session):
    # Setup test environment
    settings.TESTING = True
    
    # Import Base here to avoid circular imports
    from app.db.base_class import Base
    
    # Clean up test data before each test
    try:
        # Delete all data from tables
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")
        db.rollback()
    
    yield
    
    # Clean up test data after each test
    try:
        # Delete all data from tables
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")
        db.rollback()

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_user(db: Session):
    # First try to get existing user
    existing_user = crud_user.get_by_email(db, email="test@example.com")
    if existing_user:
        return existing_user
        
    # If no existing user, create new one
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
        "is_superuser": True
    }
    user = crud_user.create(db, obj_in=UserCreate(**user_data))
    return user

@pytest.fixture
def token(test_user):
    access_token = create_access_token(
        data={"sub": test_user.email},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return access_token

@pytest.fixture
def user_id(test_user):
    return test_user.id

@pytest.fixture
def test_learning_path_data():
    return LearningPathCreate(
        title="Test Learning Path",
        description="Test Description",
        is_public=True,
        difficulty_level="beginner",
        estimated_duration=60,
        tags=["test", "python"]
    )

@pytest.fixture
def test_learning_path_step_data():
    return LearningPathStepCreate(
        title="Test Step",
        description="Test Step Description",
        order=1,
        content_type=ContentType.TEXT,
        content_id=UUID("396c9a86-8ed9-470e-9a0e-f55a8ea10e8b"),
        learning_path_id=UUID("419790f4-6e99-4a9c-90b8-c148e96214ba")
    )

@pytest.fixture
def test_content_item_data():
    return ContentCreate(
        content_type=ContentType.TEXT,
        title="Test Content",
        content="Test content text",
        metadata={"key": "value"}
    )

@pytest.fixture
def test_user_progress_data():
    return UserProgressCreate(
        status=ProgressStatus.IN_PROGRESS,
        started_at=datetime.now(),
        learning_path_id=UUID("b024ceeb-cf2c-40e5-aeeb-c9afe3b5dc88"),
        step_id=UUID("be0b2479-8c9f-4a62-ae68-e8bb63636cab")
    )

@pytest.fixture
def test_token(test_user):
    return create_access_token(subject=test_user.email)

@pytest.fixture
def test_headers(test_token):
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture(scope="function")
def test_api_user(db):
    from app.schemas.user import UserCreate
    from app.crud.crud_user import crud_user
    email = "testapi@example.com"
    user = crud_user.get_by_email(db, email=email)
    if not user:
        user_data = UserCreate(
            email=email,
            username="testapi",
            password="testpass123",
            full_name="Test API User",
            is_superuser=True
        )
        user = crud_user.create(db, obj_in=user_data)
    access_token = create_access_token(subject=user.email)
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at) if hasattr(user, 'created_at') else None,
        "updated_at": str(user.updated_at) if hasattr(user, 'updated_at') else None,
        "access_token": access_token
    }

@pytest.fixture
def auth_token(test_token):
    return test_token