from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from ..database.prod_sql_database import SessionLocal
from ..database.models import Users
from starlette import status
from passlib.context import CryptContext
from .auth_router import verify_access_token
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_access_token)]

@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_logged_in_user(user: user_dependency, db: db_dependency):
    current_user = db.query(Users).filter(Users.user_id == UUID(user.get('user_id'))).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "data": current_user
    }

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, updated_password_payload: object=Body()):
    current_user = db.query(Users).filter(Users.user_id == UUID(user.get('user_id'))).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user.hashed_password = bcrypt_context.hash(updated_password_payload.get('new_password'))

    db.commit()

@router.put("/change_phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone(user: user_dependency, db: db_dependency, updated_phone_payload: object=Body()):
    current_user = db.query(Users).filter(Users.user_id == UUID(user.get('user_id'))).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user.phone_number = updated_phone_payload.get('phone')

    db.commit()    