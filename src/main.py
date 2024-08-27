from fastapi import FastAPI
from src.api import todo
app = FastAPI()
app.include_router(todo.router)

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}


#베이스 모델상속
        
   
