from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todos
from starlette import status
from routers.auth_router import verify_access_token

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_access_token)]

@router.get("/get_all_todos", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    role = user.get('role')
    if role == "admin":
        todos = db.query(Todos).all()
        return {
            "data": todos
        }
    raise HTTPException(status_code=401, detail="Only admin is allowed to perform this action")

@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    role = user.get("role")
    if role == "admin":
        db.query(Todos).filter(Todos.id == todo_id).delete()
        db.commit()
        return
    raise HTTPException(status_code=401, detail="Only admin is allowed to perform this action")