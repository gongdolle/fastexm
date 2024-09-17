import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.orm import User
@pytest.fixture
def client():
    return TestClient(app=app)

