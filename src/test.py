from src.database.connection import SessionFactory
from sqlalchemy import select
from src.database.orm import ToDo
session=SessionFactory()


a=list(session.scalars(select(ToDo)))
print(a)