import requests
import json

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

if __name__ == "__main__":
    # Test login
    token = test_login()
    
    if token:
        # Test /me endpoint with token
        test_me_endpoint(token) 