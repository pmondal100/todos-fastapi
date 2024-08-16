from ..routers.users_router import get_db
from ..routers.auth_router import verify_access_token
from ..main import app
from .utils import *

app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[verify_access_token] = get_test_user


def test_get_current_user(create_user):
    response = test_app.get("/users/get_user")
    assert response.status_code == 200
    assert response.json()["data"]["user_id"] == "e4d5463d-dac8-4284-9ffc-2737b773ad30"
    assert response.json()["data"]["email"] == "pmondal@gmail.com"
    assert response.json()["data"]["first_name"] == "Prabhakar"
    assert response.json()["data"]["last_name"] == "Mondal"
    assert response.json()["data"]["phone_number"] == "+918989535207"
    assert response.json()["data"]["role"] == "admin"
    assert response.json()["data"]["username"] == "pmondal"


def test_forget_password(create_user):
    updated_password_payload = {"new_password": "admin@123"}
    response = test_app.put("/users/change_password", json=updated_password_payload)
    db = TestingSessionLocal()
    user = (
        db.query(Users)
        .filter(Users.user_id == uuid.UUID("e4d5463d-dac8-4284-9ffc-2737b773ad30"))
        .first()
    )
    assert response.status_code == 204
    assert (
        bcrypt_context.verify(
            updated_password_payload.get("new_password"), user.hashed_password
        )
        is True
    )


def test_change_phone_number(create_user):
    updated_phone_payload = {"phone": "+918989535208"}
    response = test_app.put("/users/change_phone", json=updated_phone_payload)
    db = TestingSessionLocal()
    user = (
        db.query(Users)
        .filter(Users.user_id == uuid.UUID("e4d5463d-dac8-4284-9ffc-2737b773ad30"))
        .first()
    )
    assert response.status_code == 204
    assert (updated_phone_payload.get("phone") == user.phone_number) is True
