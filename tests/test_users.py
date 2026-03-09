from app.main import app

# ------ CREATE USER TESTS ------

def test_create_user(client):
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

def test_create_user_returns_422_when_email_missing(client):
    payload = {
        "name": "Test User"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 422

# ------ GET USER TESTS ------

def test_get_user_by_id_returns_user(client):
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

def test_get_user_by_id_returns_404_for_missing_user(client):
    response = client.get("/users/999")

    assert response.status_code == 404

# ------ GET USER LIST TESTS ------

def test_get_user_list_success(client):
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

def test_get_user_list_empty(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == []

def test_list_users_respects_limit(client):
    payload1 = {"email": "a@test.com", "name": "User A"}
    payload2 = {"email": "b@test.com", "name": "User B"}
    payload3 = {"email": "c@test.com", "name": "User C"}

    client.post("/users", json=payload1)
    client.post("/users", json=payload2)
    client.post("/users", json=payload3)

    response = client.get("/users?limit=2&offset=0")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["email"] == "a@test.com"
    assert data[1]["email"] == "b@test.com"

def test_list_users_respects_offset(client):
    payload1 = {"email": "a@test.com", "name": "User A"}
    payload2 = {"email": "b@test.com", "name": "User B"}
    payload3 = {"email": "c@test.com", "name": "User C"}

    client.post("/users", json=payload1)
    client.post("/users", json=payload2)
    client.post("/users", json=payload3)

    response = client.get("/users?limit=2&offset=2")

    assert response.status_code == 200 

    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "c@test.com"

# ------ PATCH TESTS/UPDATE USER ------

def test_patch_user_email_returns_200_ok(client):
    payload = {"email": "example@email.com",
               "name": "New User"}

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    payload_patch = {"email": "new@email.com"}
    patch_response = client.patch(f"/users/{user_id}", json=payload_patch)

    assert patch_response.status_code == 200

    data = patch_response.json()
    assert data["id"] == user_id
    assert data["email"] == payload_patch["email"]

def test_patch_user_email_returns_404_when_not_found(client):
    payload = {"email": "example@email.com",
               "name": "New Name"}
    response = client.patch("/users/999", json=payload)
    assert response.status_code == 404

# ------ DELETE USER TESTS ------

def test_delete_user_by_id_returns_204_success_no_content(client):
    payload = {"email": "example@email.com",
        "name": "New User"}

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")

    assert delete_response.status_code == 204
    
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_user_by_id_returns_404_when_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
