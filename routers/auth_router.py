from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..database.prod_sql_database import SessionLocal
from ..validators.body_parser import UserRequest
from ..database.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def create_access_token(data: dict, expiry_delta: timedelta):
    expiry_time = datetime.now(timezone.utc) + expiry_delta
    data_to_encode = data.copy()
    data_to_encode["exp"] = expiry_time
    return jwt.encode(
        data_to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )


def verify_access_token(
    db: db_dependency, token: Annotated[str, Depends(oauth2_bearer)]
):
    try:
        decoded_user = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        decoded_user_id = decoded_user.get("user_id")
        user = db.query(Users).filter(Users.user_id == UUID(decoded_user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Could not find the user")
        return decoded_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True,
        role=user_request.role,
    )

    db.add(user)
    db.commit()


@router.post("/login", status_code=status.HTTP_200_OK)
async def sign_in(
    db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    username = form_data.username
    password = form_data.password

    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    is_valid = bcrypt_context.verify(password, user.hashed_password)

    if not is_valid:
        raise HTTPException(status_code=401, detail="Password not valid")
    
    return {
        "access_token": create_access_token(
            {
                "username": user.username,
                "user_id": str(user.user_id),
                "role": user.role,
            },
            timedelta(int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))),
        ),
    }
