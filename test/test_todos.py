from ..routers.todos_router import get_db
from ..routers.auth_router import verify_access_token
from ..database.models import Todos
from ..main import app
from .utils import *


app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[verify_access_token] = get_test_user


def test_get_all_todos(create_todo):
    response = test_app.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": 1,
                "title": "Trim the lawn",
                "description": "Moh my dirty dirty laaawnnn",
                "priority": 4,
                "complete": False,
                "owner_id": "e4d5463d-dac8-4284-9ffc-2737b773ad30",
            }
        ]
    }


def test_get_todo_by_id(create_todo):
    response = test_app.get("/todos/1")
    response.status_code == 200
    assert response.json() == {
        "data": {
            "id": 1,
            "title": "Trim the lawn",
            "description": "Moh my dirty dirty laaawnnn",
            "priority": 4,
            "complete": False,
            "owner_id": "e4d5463d-dac8-4284-9ffc-2737b773ad30",
        }
    }


def test_get_todo_by_id_negative(create_todo):
    response = test_app.get("/todos/999")
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(create_todo):
    request_body = {
        "complete": False,
        "description": "This is my favourite book",
        "priority": 4,
        "title": "My favourite book",
    }

    response = test_app.post("/todos", json=request_body)
    assert response.status_code == 201

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 2).first()

    assert todo.title == request_body.get("title")
    assert todo.description == request_body.get("description")
    assert todo.complete == request_body.get("complete")
    assert todo.priority == request_body.get("priority")


def test_modify_todo(create_todo):
    request_body = {
        "title": "Trim the lawn",
        "description": "Trim my lawn",
        "priority": 4,
        "complete": True,
    }

    response = test_app.put("/todos/1", json=request_body)

    assert response.status_code == 204

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()

    assert todo.title == request_body.get("title")
    assert todo.description == request_body.get("description")
    assert todo.complete == request_body.get("complete")
    assert todo.priority == request_body.get("priority")


def test_modify_failed(create_todo):
    request_body = {
        "title": "Trim the lawn",
        "description": "Trim my lawn",
        "priority": 4,
        "complete": True,
    }

    response = test_app.put("/todos/999", json=request_body)

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_delete(create_todo):
    response = test_app.delete("/todos/1")

    assert response.status_code == 204
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None

def test_delete_todo_failed(create_todo):

    response = test_app.delete("/todos/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}