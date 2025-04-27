import pytest
from app.core.security import create_access_token

def test_register_user(client):
    user_data = {
        "email": "auth_test@example.com",
        "username": "authtest",
        "password": "testpass123",
        "full_name": "Auth Test User"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user(client):
    # First register
    user_data = {
        "email": "login_test@example.com",
        "username": "logintest",
        "password": "testpass123",
        "full_name": "Login Test User"
    }
    client.post("/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user(client):
    # First register and get token
    user_data = {
        "email": "current_test@example.com",
        "username": "currenttest",
        "password": "testpass123",
        "full_name": "Current Test User"
    }
    register_response = client.post("/auth/register", json=user_data)
    token = register_response.json()["access_token"]
    
    # Then get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"] 