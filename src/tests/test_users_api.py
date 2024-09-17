from fastapi.testclient import TestClient
from src.main import app
from src.database.orm import ToDo,User
from src.database.repository import ToDoRepository ,UserRepository
from src.tests.conftest import client
from src.service.user import UserService

def test_user_sign_up(client,mocker):
    hash_password=mocker.patch.object(
        UserService,
        "hash_password",
        return_value="hashed"
    )
    
    
    user_create=mocker.patch.object(
        User,
        "create",
        return_value=User(id=None,username="test",password="hashed")
    )
    
    mocker.patch.object(
        UserRepository,
        "save_user",
        return_value=User(id=1,username="test",password="hashed")
    )
    
    body={
        "username":"test",
        "password":"plain"
    }
    response=client.post("/users/sign-up",json=body)
    
    #어떤인자가지고 호출됬는지 나옴
    hash_password.asser_called_once_with(
        plain_password="plain"
        
    )
    
    user_create.asser_called_once_with(
        username="test",hashed_password="hashed"
    )
    assert response.status_code==201
    assert response.json() =={"id":1,"username":"test"}
    

