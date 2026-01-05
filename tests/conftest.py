import pytest
from app.main import user_repo

@pytest.fixture(autouse=True)
def reset_user_repo():
    user_repo.reset()
    