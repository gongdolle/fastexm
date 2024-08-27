from schema.respones import ToDoSchema
from database.orm import ToDo
from pydantic import BaseModel

todo = ToDo(id=100, contents="test", is_done=True)

a=ToDoSchema.from_orm(todo)
print(a)