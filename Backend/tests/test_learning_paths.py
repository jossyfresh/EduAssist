import pytest
from uuid import uuid4

def test_create_learning_path(client, auth_token):
    learning_path_data = {
        "title": "Test Learning Path",
        "description": "A test learning path",
        "status": "draft"
    }
    response = client.post(
        "/learning-paths/",
        json=learning_path_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == learning_path_data["title"]
    assert data["description"] == learning_path_data["description"]

def test_get_learning_paths(client, auth_token):
    response = client.get(
        "/learning-paths/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_learning_path(client, auth_token):
    # First create a learning path
    learning_path_data = {
        "title": "Test Get Path",
        "description": "A test learning path for get",
        "status": "draft"
    }
    create_response = client.post(
        "/learning-paths/",
        json=learning_path_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    path_id = create_response.json()["id"]
    
    # Then get the learning path
    response = client.get(
        f"/learning-paths/{path_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == learning_path_data["title"]
    assert data["description"] == learning_path_data["description"]

def test_get_nonexistent_learning_path(client, auth_token):
    response = client.get(
        f"/learning-paths/{uuid4()}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404 