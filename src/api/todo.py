from src.database.connection import get_db
from src.database.orm import ToDo
from src.database.repository import ToDoRepository
from src.schema.request import CreateToDoRequest
from src.schema.respones import ToDoListSchema, ToDoSchema
from fastapi import FastAPI,Body,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from src.security import get_access_token
from src.service.user import UserService
from src.database.repository import UserRepository
from typing import List


router=APIRouter(prefix="/todos")

   

@router.get("", status_code=200)
def get_todos_handler(
    access_token:str =Depends(get_access_token),
    order: str | None = None,
    todo_repo : ToDoRepository = Depends(ToDoRepository),
    user_service:UserService =Depends(),
    user_repo:UserRepository=Depends(),
) -> ToDoListSchema:
    
    username:str= user_service.decode_jwt(access_token=access_token)
    user:UserRepository|None =user_repo.get_use_by_username(username=username)
    
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found")
    
    
    
    todos: List[Todo] = user.todos

    if order and order == "DESC":
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )

    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/{todo_id}",status_code=200)
def get_todo_handler(
    todo_id: int,
    todo_repo : ToDoRepository = Depends(ToDoRepository),
    )->ToDoSchema:

    todo:Todo | None =todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)

    raise HTTPException(status_code=404,detail="ToDo Not Found")


@router.post("",status_code=201)
def create_todo_handler(
    request: CreateToDoRequest,
    todo_repo : ToDoRepository = Depends(ToDoRepository),
    
                        )->ToDoSchema:
    
    todo:ToDo =ToDo.create(request=request) #id= unknows
    todo:ToDo =todo_repo.creat_todo(todo=todo)#determine id


    return ToDoSchema.from_orm(todo)


@router.patch("/{todo_id}")
def update_todo_handler(
    todo_id: int,
    is_done:bool =Body(...,embed=True),
    todo_repo : ToDoRepository = Depends(ToDoRepository),
    ):

    todo:Todo | None =todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if todo:
        #update
        todo.done() if is_done else todo.undone()
        todo: ToDo=todo_repo.update_todo(todo=todo)
        return ToDoSchema.from_orm(todo)

    raise HTTPException(status_code=404,detail="ToDo Not Found")


@router.delete("/{todo_id}",status_code=204)
def delete_todo_handler(
    todo_id: int,
    todo_repo : ToDoRepository = Depends(ToDoRepository),
    ):
    todo:Todo | None =todo_repo.get_todo_by_todo_id(todo_id=todo_id)

    if not todo:
         raise HTTPException(status_code=404,detail="ToDo Not Found")

    todo_repo.delete_todo(todo_id=todo_id)