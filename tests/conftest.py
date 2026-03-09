import pytest
from fastapi.testclient import TestClient
from app.main import app, user_repo

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_user_repo():
    user_repo.reset()
    