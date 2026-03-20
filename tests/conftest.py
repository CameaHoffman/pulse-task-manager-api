import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app, user_repo, project_repo, task_repo

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_repositories():
    task_repo.reset()
    project_repo.reset()
    user_repo.reset()
    
@pytest.fixture
def auth_headers(client):
    email = f"tester_{uuid.uuid4().hex}@example.com"

    user_payload = {
        "email": email,
        "name": "Tester",
        "password": "securepassword"
    }
    
    create_response = client.post("/users", json=user_payload)
    assert create_response.status_code == 201, create_response.text

    login_data = {
        "username": email,
        "password": "securepassword"
    }

    login_response = client.post("/token", data=login_data)
    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}