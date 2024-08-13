from ..database.test_database_config import Base, engine, TestingSessionLocal
from ..routers.todos_router import get_db
from ..routers.auth_router import verify_access_token
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..database.models import Todos
import uuid


def get_test_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


def get_test_user():
    return {
        "username": "pmondal",
        "user_id": "e4d5463d-dac8-4284-9ffc-2737b773ad30",
        "role": "admin",
    }


app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[verify_access_token] = get_test_user

test_app = TestClient(app)


@pytest.fixture
def create_todo():
    todo = Todos(
        id=1,
        title="Trim the lawn",
        description="Moh my dirty dirty laaawnnn",
        priority=4,
        complete=False,
        owner_id=uuid.UUID("e4d5463d-dac8-4284-9ffc-2737b773ad30"),
    )
    test_db = TestingSessionLocal()
    test_db.add(todo)
    test_db.commit()
    yield todo
    test_db.delete(todo)
    test_db.commit()
    test_db.close()


def test_get_all_todos(create_todo):
    response = test_app.get("/todos")
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
