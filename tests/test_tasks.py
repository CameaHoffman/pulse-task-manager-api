from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ------ CREATE TASK TESTS ------
def test_create_task_returns_201_created():

    payload = {
        "name": "New Project",
        "description": "Project description."
    }

    create_response = client.post("/projects", json=payload)

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    payload = {"title": "New Task",
               "description": "Task description.",
               "project_id": project_id
    }
    
    task_response = client.post("/tasks", json=payload)

    assert task_response.status_code == 201
    
    task_id = task_response.json()["id"]

    data = task_response.json()

    assert "id" in data
    assert data["id"] == task_id
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]

# ------ GET TASK TESTS ------
# ------ UPDATE TASK TESTS ------
# ------ DELETE TASK TESTS ------