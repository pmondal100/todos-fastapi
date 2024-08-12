from fastapi import FastAPI
import models
from database import engine
from starlette import status
from routers.todos_router import router as todos_router
from routers.auth_router import router as auth_router
from routers.admin_router import router as admin_router
from routers.users_router import router as users_router
from routers.mongo_sample_router import  router as mongo_sample_router
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

models.Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
async def greetings():
    return {"message": "Welcome to the Todos application"}

app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(admin_router)
app.include_router(users_router)
app.include_router(mongo_sample_router)