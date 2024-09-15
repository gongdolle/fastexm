from sqlalchemy.schema import CreateTable
from src.database.orm import ToDo,User
from src.database.connection import engine

print(CreateTable(User.__table__).compile(engine))