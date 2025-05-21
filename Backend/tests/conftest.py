import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from uuid import UUID
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
from app.db.session import SessionLocal
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate

# Set test environment variables
os.environ["TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["OPENAI_API_KEY"] = "test-openai-key"
os.environ["GEMINI_API_KEY"] = "test-gemini-key"

@pytest.fixture(scope="module")
def client() -> TestClient:
    """Test client fixture."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    # Setup test environment
    settings.TESTING = True
    
    # Clean up test data before each test
    try:
        # Use SQLAlchemy to clean up test data
        pass
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")
    
    yield
    
    # Clean up test data after each test
    try:
        # Use SQLAlchemy to clean up test data
        pass
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")

@pytest.fixture(scope="session")
def test_user():
    db = SessionLocal()
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpassword",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    user = crud_user.get_by_email(db, email=user_in.email)
    if not user:
        user = crud_user.create(db, obj_in=user_in)
    db.close()
    user_data = {
        "id": user.email,  # use email as id for token
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }
    return user_data

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
        step_order=1,
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
def test_user_id():
    return "bd56ad3b-d644-4cab-8e9c-6113ca46f4ec"

@pytest.fixture
def test_token(test_user):
    """Create a test JWT token."""
    return create_access_token(subject=test_user["id"])

@pytest.fixture
def test_headers(test_token):
    """Create test headers with JWT token."""
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture(scope="session")
def test_api_user():
    user_data = {
        "id": "testapi@example.com",  # use email as id
        "email": "testapi@example.com",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    access_token = create_access_token(subject=user_data["id"])
    user_data["access_token"] = access_token
    return user_data

@pytest.fixture(scope="function")
def db():
    """Create a fresh database session for a test."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 