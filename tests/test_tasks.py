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

# ------ GET TASKS LIST TEST -------   

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

def test_patch_task_title_returns_200_ok():
    payload = {"name": "Project One"}

    project_response = client.post("/projects", json=payload)

    assert project_response.status_code == 201

    project_id = project_response.json()["id"]
    
    task_payload = {"title": "Task One",
               "project_id": project_id}

    create_response = client.post("/tasks", json=task_payload)
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    payload_patch = {"title": "New Title"}
    patch_response = client.patch(f"/tasks/{task_id}",
                                  json=payload_patch)

    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == task_id
    assert data["title"] == payload_patch["title"]
    assert data["project_id"] == project_id

def test_patch_task_title_returns_404_when_not_found():
    payload = {"title": "New Title"}
    response = client.patch("/tasks/999", json=payload)
    assert response.status_code == 404

def test_patch_task_is_done_returns_200_ok():
    project = client.post("/projects", json={"name": "Project One"})
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id})
    task_id = created.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"is_done": True})
    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == task_id
    assert data["is_done"] is True

def test_patch_task_is_done_returns_404_when_not_found():
    response = client.patch("/tasks/999", json={"is_done": True})
    assert response.status_code == 404

def test_patch_with_multiple_fields_updates_all_changes():
    project = client.post("/projects", json={"name": "Project One"})
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id})
    task_id = created.json()["id"]

    payload = {"title": "Task Update", "is_done": True}
    patch_response = client.patch(f"/tasks/{task_id}", json=payload)
    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["title"] == payload["title"]
    assert data["is_done"] is True

def test_patch_with_no_fields_returns_400():
    project = client.post("/projects", json={"name": "Project One"})
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id})
    task_id = created.json()["id"]

    payload = {"title": None, "description": None}
    patch_response = client.patch(f"/tasks/{task_id}", json=payload)

    assert patch_response.status_code == 400

# ------ DELETE TASK TESTS ------

def test_delete_task_by_id_returns_204_success_no_content():
    payload = {"name": "Project One"}
    project_response = client.post("/projects", json=payload)
    project_id = project_response.json()["id"]

    task_payload = {"title": "Task to delete",
                    "project_id": project_id
                    }
    create_response = client.post("tasks", json=task_payload)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

def test_delete_task_by_id_returns_404_when_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

