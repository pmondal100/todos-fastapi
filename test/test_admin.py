from ..routers.admin_router import get_db
from ..routers.auth_router import verify_access_token
from ..main import app
from .utils import *

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[verify_access_token] = get_test_user

def test_get_all_todos(create_todo):
    response = test_app.get("/admin/get_all_todos")
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

def test_delete_admin(create_todo):
    response = test_app.delete("/admin/delete_todo/1")

    assert response.status_code == 204
    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None

def test_delete_todo_failed_admin(create_todo):
    response = test_app.delete("/admin/delete_todo/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}