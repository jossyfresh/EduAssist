import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.supabase import supabase
from uuid import UUID
from datetime import datetime
from app.core.security import create_access_token
from app.models.learning_path import (
    LearningPathCreate,
    LearningPathStepCreate,
    ContentItemCreate,
    UserProgressCreate,
    ContentType,
    ProgressStatus
)

# Set test environment variables
os.environ["TESTING"] = "True"
os.environ["SUPABASE_URL"] = "https://jtqoyyjrkdxcvlbytblw.supabase.co"
os.environ["SUPABASE_SERVICE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp0cW95eWpya2R4Y3ZsYnl0Ymx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Mjg4NTQ2OCwiZXhwIjoyMDU4NDYxNDY4fQ.5mWVjw3ySoTaeO3CaTiQh1xKH_Dpc0Ogw-9nOz2ZKGA"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["OPENAI_API_KEY"] = "test-openai-key"

@pytest.fixture(scope="module")
def client() -> TestClient:
    """Test client fixture."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="module")
def supabase_client():
    """Supabase client fixture."""
    return supabase

@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    # Setup test environment
    settings.TESTING = True
    
    # Clean up test data before each test
    try:
        supabase.table("learning_paths").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("learning_path_steps").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("content_items").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("user_progress").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")
    
    yield
    
    # Clean up test data after each test
    try:
        supabase.table("learning_paths").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("learning_path_steps").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("content_items").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        supabase.table("user_progress").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")

@pytest.fixture(scope="session")
def test_user():
    # Create a test user in Supabase
    user_data = {
        "id": "f53783aa-84ea-4bc0-99e7-b59b9a184396",
        "email": "test@example.com",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Delete user if exists
    supabase.table("users").delete().eq("id", user_data["id"]).execute()
    
    # Create new user
    result = supabase.table("users").insert(user_data).execute()
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
    return ContentItemCreate(
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
    return create_access_token(data={"sub": test_user["id"]})

@pytest.fixture
def test_headers(test_token):
    """Create test headers with JWT token."""
    return {"Authorization": f"Bearer {test_token}"}

@pytest.fixture(scope="session")
def test_api_user():
    # Create a test user in Supabase for API tests
    user_data = {
        "id": "bd56ad3b-d644-4cab-8e9c-6113ca46f4ec",
        "email": "testapi@example.com",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Delete user if exists
    supabase.table("users").delete().eq("id", user_data["id"]).execute()
    
    # Create new user
    result = supabase.table("users").insert(user_data).execute()
    
    # Create access token
    access_token = create_access_token({"sub": user_data["id"]})
    user_data["access_token"] = access_token
    
    return user_data 