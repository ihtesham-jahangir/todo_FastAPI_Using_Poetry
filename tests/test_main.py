from http import client
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from datetime import datetime
from todo.main import app, get_session, Todo
from todo import settings

def test_read_main():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_write_main():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)

        task_id = "01"
        user_id =  "00001"
        task_name = "Assignments "
        Description = "First Assignment : CN "
        Priority =  "1"
        Completed_task = "1"
        due_date = datetime.now()
        response = client.post(
            "/todos/",
            json={"task_id": task_id, "user_id": user_id, "date": due_date , "task_name": task_name , "Description": Description , "Priority":Priority , "Completed_Task":Completed_task},
        )

        data = response.json()

        assert response.status_code == 200
        assert data["task_name"] == task_name

def test_read_list_main():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/todos/")
        assert response.status_code == 200

def test_write_main1():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)

        user_id =  1
        pswd = "12345678"

        response = client.post(
            "/users/",
            json={"user_id": user_id, "pswd": pswd},
        )

        data = response.json()

        assert response.status_code == 200
        assert data["user_id"] == user_id

def test_update_todo():
    
    task_data = {"task_name": "Test Task", "Description": "Test Description", "Priority": 1}
    response = client.post("/todos/", json=task_data)
    assert response.status_code == 200
    created_todo = response.json()
    
   
    updated_data = {"task_name": "Updated Task", "Description": "Updated Description", "Priority": 2}
    response = client.put(f"/todos/{created_todo['task_id']}", json=updated_data)
    assert response.status_code == 200
    updated_todo = response.json()
    
   
    assert updated_todo["task_name"] == updated_data["task_name"]
    assert updated_todo["Description"] == updated_data["Description"]
    assert updated_todo["Priority"] == updated_data["Priority"]

def test_delete_todo():
   
    task_data = {"task_name": "Test Task", "Description": "Test Description", "Priority": 1}
    response = client.post("/todos/", json=task_data)
    assert response.status_code == 200
    created_todo = response.json()
    
  
    response = client.delete(f"/todos/{created_todo['task_id']}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Todo with ID {created_todo['task_id']} deleted successfully"}

    
    response = client.get("/todos/")
    assert response.status_code == 200
    todos = response.json()
    assert not any(todo["task_id"] == created_todo["task_id"] for todo in todos)


def test_read_list_main1():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/users/")
        assert response.status_code == 200


def test_write_category():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)

        category_id =  1
        category_name = "test"

        response = client.post(
            "/category/",
            json={"category_id": category_id, "category_name": category_name},
        )

        data = response.json()

        assert response.status_code == 200
        assert data["category_id"] == category_id

def test_read_list_category():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/category/")
        assert response.status_code == 200


def test_write_tag():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)

        tag_id =  1
        tag_name = "test"

        response = client.post(
            "/tag/",
            json={"tag_id": tag_id, "tag_name": tag_name},
        )

        data = response.json()

        assert response.status_code == 200
        assert data["tag_id"] == tag_id

def test_read_list_tag():
    connection_string = settings.TEST_DATABASE_URL.replace(
        "postgresql", "postgresql+psycopg2"
    )

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)

        response = client.get("/tag/")
        assert response.status_code == 200


