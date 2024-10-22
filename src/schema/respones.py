from pydantic import BaseModel,EmailStr
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
    email:str
    role_id:int
    name:str
    phone_num:str
    company_code:str
    class Config:
        orm_mode = True
        
        
class JWTResponse(BaseModel):
    access_token:str

class TnFResppnse(BaseModel):
    TnF: bool 