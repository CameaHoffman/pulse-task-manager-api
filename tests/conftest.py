import pytest
from fastapi.testclient import TestClient
from app.main import app, user_repo, project_repo, task_repo

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_repositories():
    user_repo.reset()
    project_repo.reset()
    task_repo.reset()
    