from fastapi.testclient import TestClient
from src.main import app
from src.database.orm import ToDo
from src.database.repository import ToDoRepository 
from src.tests.conftest import client

def test_health_check(client):
    response=client.get("/")
    assert response.status_code== 200
    assert response.json()=={"ping":"pong"}