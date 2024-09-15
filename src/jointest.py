from src.database.connection import SessionFactory
from src.database.orm import User
from sqlalchemy import select

session=SessionFactory()

user=session.scalar(select(User))
print(user.todos)