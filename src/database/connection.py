from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL="mysql+pymysql://root:todos@127.0.0.1:3306/todos"


engine=create_engine(DATABASE_URL,echo=True)


SessionFactory=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#제네레이터로 인스턴스 생성후 yield로 반환과 동시에 굳어있다가 자동닫기됨
def get_db():
    session=SessionFactory()
    try:
        yield session
    finally :
        session.close()
        
