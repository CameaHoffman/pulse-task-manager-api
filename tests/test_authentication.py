from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_token_login_success():
    #create user
    payload = {
        "email": "auth_test@example.com",
        "name": "Auth Test",
        "password": "securepassword"
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    #attempt login
    login_data = {
        "username": "auth_test@example.com",
        "password": "securepassword"

    }

    login_response = client.post("/token", data=login_data)

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_token_login_failure():
    #create user
    payload = {
        "email": "auth_test@example.com",
        "name": "Auth Test",
        "password": "securepassword"
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    #attempt login with incorrect password
    login_data = {
        "username": "auth_test@example.com",
        "password": "wrongpassword"
    }

    login_response = client.post("/token", data=login_data)

    assert login_response.status_code == 401

    data = login_response.json()
    assert data["detail"] == "Incorrect username or password"

