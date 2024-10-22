from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import todo,user
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://p-gridon.com"],  # React 프론트엔드 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todo.router)
app.include_router(user.router)

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

