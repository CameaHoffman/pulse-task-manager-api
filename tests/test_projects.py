from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project_returns_201():
    payload = {
        "name": "New Project",
        "description": "Project description."
    }

    response = client.post("/projects", json=payload)

    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_get_project_by_id_returns_200():
    payload = {
        "name": "New Project",
        "description": "Project description."
    }

    create_response = client.post("/projects", json=payload)
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["id"] == project_id
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_lists_projects_returns_projects():
    payload1 = {"name": "Project One"}
    payload2 = {"name": "Project Two"}

    client.post("/projects", json=payload1)
    client.post("/projects", json=payload2)

    response = client.get("/projects")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

