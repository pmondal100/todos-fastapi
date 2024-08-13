from fastapi import APIRouter, Depends, HTTPException
from ..database.mongo_database_config import db, client
from typing import Annotated
from ..validators.body_parser import MongoSampleRequest
from passlib.context import CryptContext
from .auth_router import verify_access_token
from bson import ObjectId
from starlette import status

router = APIRouter(prefix="/mongo_sample", tags=["Mongo_Sample"])
user_dependency = Annotated[dict, Depends(verify_access_token)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    try:
        yield db
    finally:
        client.close()

def convert_objectid(obj):
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    if isinstance(obj, dict):
        return {key: convert_objectid(value) for key, value in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db= Depends(get_db)):
    all_users = await db.Users.find().to_list(length=None)
    if all_users is None:
        raise HTTPException(status_code=500, detail="Intenal server error")
    all_users = convert_objectid(all_users)
    return {
        "data": all_users
    }

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(user_req: MongoSampleRequest, user: user_dependency, db= Depends(get_db)):
    req_dict = user_req.model_dump()
    req_dict["password"] = bcrypt_context.hash(req_dict.get("password"))
    res = await db.Users.insert_one(req_dict)
    if res is None:
        raise HTTPException(status_code=500, detail="Intenal server error")
    