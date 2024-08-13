from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from ..database.prod_sql_database import SessionLocal
from ..database.models import Todos
from starlette import status
from ..validators.body_parser import TodosRequest
from .auth_router import verify_access_token
from uuid import UUID

router = APIRouter(prefix="/todos", tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_access_token)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    all_todos = (
        db.query(Todos).filter(Todos.owner_id == UUID(user.get("user_id"))).all()
    )
    return {"data": all_todos}


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo = (
        db.query(Todos)
        .filter(Todos.owner_id == UUID(user.get("user_id")))
        .filter(Todos.id == todo_id)
        .first()
    )

    if todo is not None:
        return {"data": todo}

    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodosRequest
):
    todo_data = todo_request.model_dump()
    todo_data["owner_id"] = UUID(user.get("user_id"))
    db.add(Todos(**todo_data))
    db.commit()

    return {"data": todo_request}


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency, db: db_dependency, todo_request: TodosRequest, todo_id: int = Path(gt=0)
):
    todo = db.query(Todos).filter(Todos.owner_id == UUID(user.get("user_id"))).filter(Todos.id == todo_id).first()

    if todo is not None:
        todo.title = todo_request.title
        todo.description = todo_request.description
        todo.priority = todo_request.priority
        todo.complete = todo_request.complete
        db.commit()
        return {"data": todo_request}

    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.owner_id == UUID(user.get("user_id"))).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    return {"data": todo}
