import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_generate_content(client):
    response = client.post(
        "/generate",
        json={
            "topic": "Python Programming",
            "content_type": "lesson",
            "difficulty": "beginner",
            "target_audience": "high school students"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "metadata" in data
    assert data["metadata"]["topic"] == "Python Programming"
    assert data["metadata"]["content_type"] == "lesson"
    assert data["metadata"]["difficulty"] == "beginner"
    assert data["metadata"]["target_audience"] == "high school students"

def test_generate_content_invalid_type(client):
    response = client.post(
        "/generate",
        json={
            "topic": "Python Programming",
            "content_type": "invalid_type",
            "difficulty": "beginner",
            "target_audience": "high school students"
        }
    )
    assert response.status_code == 422

def test_generate_content_missing_fields(client):
    response = client.post(
        "/generate",
        json={
            "topic": "Python Programming"
        }
    )
    assert response.status_code == 422 