import pytest
from uuid import uuid4
import requests
import json
import time

def test_create_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]

def test_get_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user(client):
    # First create a user
    user_data = {
        "email": "test2@example.com",
        "username": "testuser2",
        "full_name": "Test User 2"
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Then get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

def test_get_nonexistent_user(client):
    response = client.get(f"/users/{uuid4()}")
    assert response.status_code == 404

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_login():
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "rebumatadele4@gmail.com",
        "password": "rebu4213"
    }
    try:
        response = requests.post(url, json=data)
        print("Login Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
            return response.json().get("access_token")
        else:
            print("Error:", response.text)
            return None
    except Exception as e:
        print("Login Error:", str(e))
        return None

def test_me_endpoint(token):
    url = f"{BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        print("\nMe Endpoint Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Me Endpoint Error:", str(e))

def test_list_users(token):
    url = f"{BASE_URL}/users"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        print("\nList Users Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print("List Users Error:", str(e))

def test_get_user(token, user_id):
    url = f"{BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"\nGet User {user_id} Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Get User {user_id} Error:", str(e))

def test_create_user(token):
    url = f"{BASE_URL}/users"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword123",
        "full_name": "New User"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        print("\nCreate User Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Create User Error:", str(e))

def test_update_user(token, user_id):
    url = f"{BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "full_name": "Updated User"
    }
    try:
        response = requests.put(url, headers=headers, json=data)
        print(f"\nUpdate User {user_id} Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Update User {user_id} Error:", str(e))

def test_delete_user(token, user_id):
    url = f"{BASE_URL}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.delete(url, headers=headers)
        print(f"\nDelete User {user_id} Response:", response.status_code)
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Delete User {user_id} Error:", str(e))

if __name__ == "__main__":
    token = test_login()
    if token:
        test_me_endpoint(token)
        time.sleep(1)
        test_list_users(token)
        time.sleep(1)
        test_get_user(token, 1)
        time.sleep(1)
        test_create_user(token)
        time.sleep(1)
        test_update_user(token, 1)
        time.sleep(1)
        test_delete_user(token, 1) 