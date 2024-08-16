from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from ..main import app
import pytest
from ..database.models import Todos, Users
from sqlalchemy.orm import sessionmaker
from ..database.prod_sql_database import Base
from ..routers.users_router import bcrypt_context
import uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_todos_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(
    bind=engine
)  # Do not do declarative_base() as there can only be one time declaration and that is done in prod DB


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


test_app = TestClient(app)


@pytest.fixture
def create_todo():
    todo = Todos(
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
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def create_user():
    user = Users(
        user_id = uuid.UUID("e4d5463d-dac8-4284-9ffc-2737b773ad30"),
        email="pmondal@gmail.com",
        first_name="Prabhakar",
        last_name="Mondal",
        hashed_password=bcrypt_context.hash("admin@1234"),
        phone_number="+918989535207",
        role="admin",
        username="pmondal",
    )
    test_db = TestingSessionLocal()
    test_db.add(user)
    test_db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
