from app.main import app

# ------ CREATE TASK TESTS ------
def test_create_task_returns_201_created(client, auth_headers):

    payload = {
        "name": "New Project",
        "description": "Project description."
    }

    create_response = client.post("/projects", json=payload, headers=auth_headers)

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    payload = {"title": "New Task",
               "description": "Task description.",
               "project_id": project_id
    }
    
    task_response = client.post("/tasks", json=payload, headers=auth_headers)

    assert task_response.status_code == 201
    
    task_id = task_response.json()["id"]

    data = task_response.json()

    assert "id" in data
    assert data["id"] == task_id
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]

# ------ GET TASK TESTS ------

def test_get_task_by_id_returns_200(client, auth_headers):

    payload = {
        "name": "New Project",
        "description": "Project description."
    }

    create_response = client.post("/projects", json=payload, headers=auth_headers)

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    payload = {"title": "New Task",
               "description": "Task description.",
               "project_id": project_id
    }
    
    response = client.post("/tasks", json=payload, headers=auth_headers)

    assert response.status_code == 201

    task_id = response.json()["id"]

    task_response = client.get(f"/tasks/{task_id}")

    assert task_response.status_code == 200

    data = task_response.json()

    assert data["id"] == task_id
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["project_id"] == project_id

def test_get_task_by_id_returns_404_not_found(client):
    response = client.get("/tasks/999/")
    assert response.status_code == 404

# ------ GET TASKS LIST TESTS ------   

def test_get_tasks_list_by_project_id_returns_tasks(client, auth_headers):
    payload = {"name": "Project One"}

    create_response = client.post("/projects", json=payload, headers=auth_headers)

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

    assert client.post("/tasks", json=payload1, headers=auth_headers).status_code == 201
    assert client.post("/tasks", json=payload2, headers=auth_headers).status_code == 201

    response = client.get(f"/projects/{project_id}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    titles = [t["title"] for t in data]
    assert "First Task" in titles
    assert "Second Task" in titles
    assert all(t["project_id"] == project_id for t in data)

def test_list_tasks_respects_limit(client, auth_headers):
    project_response = client.post("/projects", json={"name": "Project One"}, headers=auth_headers)
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    payload1 = {
        "title": "First Task",
        "description": "Task description.",
        "project_id": project_id
    }

    payload2 = {
        "title": "Second Task",
        "description": "Task description.",
        "project_id": project_id
    }

    payload3 = {
        "title": "Third Task",
        "description": "Task description.",
        "project_id": project_id
    }

    client.post("/tasks", json=payload1, headers=auth_headers)
    client.post("/tasks", json=payload2, headers=auth_headers)
    client.post("/tasks", json=payload3, headers=auth_headers)

    response = client.get("/tasks?limit=2&offset=0")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

def test_list_tasks_respects_limit_and_offset(client, auth_headers):
    payload = {"name": "Project One"}
    create_response = client.post("projects", json=payload, headers=auth_headers)
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

    client.post("/tasks", json=payload1, headers=auth_headers)
    client.post("/tasks", json=payload2, headers=auth_headers)

    response = client.get(f"/projects/{project_id}/tasks?limit=1&offset=1")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Second Task"
    assert data[0]["project_id"] == project_id
 
# ------ UPDATE TASK TESTS ------

def test_patch_task_title_returns_200_ok(client, auth_headers):
    payload = {"name": "Project One"}

    project_response = client.post("/projects", json=payload, headers=auth_headers)

    assert project_response.status_code == 201

    project_id = project_response.json()["id"]
    
    task_payload = {"title": "Task One",
               "project_id": project_id}

    create_response = client.post("/tasks", json=task_payload, headers=auth_headers)
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    payload_patch = {"title": "New Title"}
    patch_response = client.patch(f"/tasks/{task_id}",
                                  json=payload_patch, headers=auth_headers)

    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == task_id
    assert data["title"] == payload_patch["title"]
    assert data["project_id"] == project_id

def test_patch_task_title_returns_404_when_not_found(client, auth_headers):
    payload = {"title": "New Title"}
    response = client.patch("/tasks/999", json=payload, headers=auth_headers)
    assert response.status_code == 404

def test_patch_task_is_done_returns_200_ok(client, auth_headers):
    project = client.post("/projects", json={"name": "Project One"}, headers=auth_headers)
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id}, headers=auth_headers)
    task_id = created.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"is_done": True}, headers=auth_headers)
    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == task_id
    assert data["is_done"] is True

def test_patch_task_is_done_returns_404_when_not_found(client, auth_headers):
    response = client.patch("/tasks/999", json={"is_done": True}, headers=auth_headers)
    assert response.status_code == 404

def test_patch_with_multiple_fields_updates_all_changes(client, auth_headers):
    project = client.post("/projects", json={"name": "Project One"}, headers=auth_headers)
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id}, headers=auth_headers)
    task_id = created.json()["id"]

    payload = {"title": "Task Update", "is_done": True}
    patch_response = client.patch(f"/tasks/{task_id}", json=payload, headers=auth_headers)
    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["title"] == payload["title"]
    assert data["is_done"] is True

def test_patch_with_no_fields_returns_400(client, auth_headers):
    project = client.post("/projects", json={"name": "Project One"}, headers=auth_headers)
    project_id = project.json()["id"]

    created = client.post("/tasks", json={"title": "Task One", "project_id": project_id}, headers=auth_headers)
    task_id = created.json()["id"]

    payload = {"title": None, "description": None}
    patch_response = client.patch(f"/tasks/{task_id}", json=payload, headers=auth_headers)

    assert patch_response.status_code == 400

# ------ DELETE TASK TESTS ------

def test_delete_task_by_id_returns_204_success_no_content(client, auth_headers):
    payload = {"name": "Project One"}
    project_response = client.post("/projects", json=payload, headers=auth_headers)
    project_id = project_response.json()["id"]

    task_payload = {"title": "Task to delete",
                    "project_id": project_id
                    }
    create_response = client.post("tasks", json=task_payload, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

def test_delete_task_by_id_returns_404_when_not_found(client, auth_headers):
    response = client.delete("/tasks/999", headers=auth_headers)
    assert response.status_code == 404

