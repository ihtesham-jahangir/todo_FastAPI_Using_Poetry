# main.py
from contextlib import asynccontextmanager
from http.client import HTTPException
from typing import Union, Optional, Annotated
from todo import settings
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, Depends
from datetime import datetime

class Users(SQLModel, table=True):
    user_id: Optional[int] = Field(default = None , primary_key = True)
    pswd: str = Field(default = None)

class Todo(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default = None , foreign_key = 'users.user_id' , unique = True)
    task_name:str = Field(index = True)
    Description:str = Field(index = None)
    Priority:int = Field(default = None)
    Completed_task:bool = Field(default = False)
    due_date: datetime = Field(default=None, index=True)
class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(default = None , primary_key = True)
    category_name: str = Field(default = None)
class Tag(SQLModel, table=True):
    tag_id: Optional[int] = Field(default = None , primary_key = True)
    tag_name: str = Field(default = None)

    
user: Optional[Users] = relationship("Users", backref="todos")

# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Wait a sec we work on it .... ")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="FastApi TODO System Created by ihtesham jahangir", 
    version="0.0.1",
    servers=[
        {
            "url": "https://a0cb-2400-adca-115-4100-cff-2fbb-7beb-1506.ngrok-free.app", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos

@app.put("/todos/{task_id}", response_model=Todo)
def update_todo(task_id: int, todo: Todo, session: Session = Depends(get_session)):
    db_todo = session.get(Todo, task_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# Endpoint to delete a todo by ID
@app.delete("/todos/{task_id}")
def delete_todo(task_id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, task_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": f"Todo with ID {task_id} deleted successfully"}


@app.post("/users/", response_model=Users)
def create_users(user: Users, session: Annotated[Session, Depends(get_session)]):
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/", response_model=list[Users])
def read_users(session: Annotated[Session, Depends(get_session)]):
        users = session.exec(select(Users)).all()
        return users

@app.post("/category/", response_model=Category)
def create_category(cat: Category, session: Annotated[Session, Depends(get_session)]):
        session.add(cat)
        session.commit()
        session.refresh(cat)
        return cat


@app.get("/category/", response_model=list[Category])
def read_category(session: Annotated[Session, Depends(get_session)]):
        category = session.exec(select(Category)).all()
        return category

@app.post("/tag/", response_model=Tag)
def create_tag(tag: Tag, session: Annotated[Session, Depends(get_session)]):
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag


@app.get("/tag/", response_model=list[Tag])
def read_tag(session: Annotated[Session, Depends(get_session)]):
        tag = session.exec(select(Tag)).all()
        return tag
