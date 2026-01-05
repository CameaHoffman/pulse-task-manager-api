from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    payload = {
        "email": "test@example.com",
        "name": "Test User"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]

def test_get_user_by_id_returns_user():
    payload = {
        "email": "test@example.com",
        "name": "Test User"
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == user_id
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]

def test_get_user_by_id_returns_404_for_missing_user():
    response = client.get("/users/999")

    assert response.status_code == 404

def test_get_user_list_success():
    payload = {
        "email": "test@example.com",
        "name": "Test User"
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    get_response = client.get("/users")
    assert get_response.status_code == 200

    users = get_response.json()
    assert len(users) == 1
    assert users[0]["email"] == payload["email"]

def test_get_user_list_empty():
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == []

