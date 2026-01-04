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



