from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ------ CREATE PROJECT TESTS ------

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

# ------ GET PROJECT BY ID TESTS------

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

# ------ GET PROJECT LIST TESTS ------

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

def test_get_project_returns_404_when_not_found():
    response = client.get("/projects/999")
    assert response.status_code == 404

# ------ PATCH TESTS/UPDATE PROJECT ------

def test_patch_project_name_returns_200_ok():
    payload = {"name": "Project One"}

    create_response = client.post("/projects", json=payload)
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    payload_patch = {"name": "New Name"}
    patch_response = client.patch(f"/projects/{project_id}", json=payload_patch)

    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == project_id
    assert data["name"] == payload_patch["name"]

def test_patch_project_name_returns_404_when_not_found():
    payload = {"name": "New Name"}
    response = client.patch("/projects/999", json=payload)
    assert response.status_code == 404

# ------ TEST DELETE PROJECT ------

def test_delete_project_by_id_returns_204_success_no_content():
    payload = {"name": "New Project"}

    create_response = client.post("/projects", json=payload)
    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    delete_response = client.delete(f"/projects/{project_id}")

    assert delete_response.status_code == 204
    
    get_response = client.get(f"/projects/{project_id}")
    assert get_response.status_code == 404

def test_delete_project_by_id_returns_404_when_not_found():
    response = client.delete("/projects/999")
    assert response.status_code == 404