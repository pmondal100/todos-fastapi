from fastapi.testclient import TestClient
from starlette import status
from ..main import app
from ..database.test_database_config import SessionLocal

test_app = TestClient(app)

def test_welcome_api():
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the Todos application"}
 
