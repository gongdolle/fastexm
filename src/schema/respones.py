from pydantic import BaseModel
from typing import List

class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool  # 필드 이름 수정
    class Config:
        orm_mode = True

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]
    
class UserSchema(BaseModel):
    id: int
    username:str
    class Config:
        orm_mode = True