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

def test_get_task_by_id_returns_200():

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
    
    response = client.post("/tasks", json=payload)

    assert response.status_code == 201

    task_id = response.json()["id"]

    task_response = client.get(f"/tasks/{task_id}")

    assert task_response.status_code == 200

    data = task_response.json()

    assert data["id"] == task_id
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["project_id"] == project_id

def test_get_task_by_id_returns_404_not_found():
    response = client.get("/tasks/999/")
    assert response.status_code == 404

# ------ GET TASKS LISTS TEST -------   

def test_get_tasks_list_by_project_id_returns_tasks():
    payload = {"name": "Project One"}

    create_response = client.post("/projects", json=payload)

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    payload1 = {"title": "First Task",
               "description": "Task description.",
               "project_id": project_id
    }

    payload2 = {"title": "Second Task",
               "description": "Task description.",
               "project_id": project_id
    }

    assert client.post("/tasks", json=payload1).status_code == 201
    assert client.post("/tasks", json=payload2).status_code == 201

    response = client.get(f"/projects/{project_id}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    titles = [t["title"] for t in data]
    assert "First Task" in titles
    assert "Second Task" in titles
    assert all(t["project_id"] == project_id for t in data)
 
# ------ UPDATE TASK TESTS ------

# ------ DELETE TASK TESTS ------