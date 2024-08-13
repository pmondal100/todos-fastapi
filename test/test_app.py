from fastapi.testclient import TestClient
from starlette import status
from ..main import app

test_app = TestClient(app)

def test_welcome_api():
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to the Todos application"}
 
