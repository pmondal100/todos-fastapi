from datetime import datetime, timedelta, timezone
from fastapi import Depends
from jose import jwt
from ..routers.auth_router import get_db
import os
from .utils import *
from dotenv import load_dotenv

load_dotenv()

app.dependency_overrides[get_db] = get_test_db


def test_create_user():
    request_body = {
        "email": "rahul.sharma@example.com",
        "first_name": "Rahul",
        "last_name": "Sharma",
        "password": "admin@1234",
        "phone_number": "+919876543210",
        "role": "admin",
        "username": "rahuls",
    }

    response = test_app.post("/auth/", json=request_body)
    assert response.status_code == 201

    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.username == "rahuls").first()

    print(user)


def test_authentication(create_user):
    form_data = {"username": "pmondal", "password": "admin@1234"}
    response = test_app.post("/auth/login", data=form_data)

    assert response.status_code == 200

    decoded_obj = jwt.decode(response.json().get("access_token"), os.getenv("SECRET_KEY"))

    assert decoded_obj.get("username") == "pmondal"
    assert decoded_obj.get("user_id") == "e4d5463d-dac8-4284-9ffc-2737b773ad30"
    assert decoded_obj.get("role") == "admin"

def test_authentication_failed(create_user):
    form_data = {"username": "pmondal", "password": "admin@1234567"}
    response = test_app.post("/auth/login", data=form_data)

    assert response.status_code == 401