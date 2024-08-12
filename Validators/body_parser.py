from uuid import UUID
from pydantic import Field, BaseModel, EmailStr


class TodosRequest(BaseModel):
    title: str = Field(min_length=5, max_length=20)
    description: str = Field(min_length=5, max_length=50)
    priority: int = Field(gt=0)
    complete: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My favourite book",
                "description": "This is my favourite book",
                "priority": 4,
                "complete": False,
            }
        }
    }


class UserRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=5, max_length=10)
    first_name: str = Field(min_length=5, max_length=10)
    last_name: str = Field(min_length=3, max_length=15)
    password: str
    role: str
    phone: int = Field(
        pattern=r"^\+?[1-9]\d{1,14}$",
        description="A valid phone number starting with an optional '+' and followed by 1 to 15 digits.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "someemail@gmail.com",
                "username": "someuser",
                "first_name": "fname",
                "last_name": "lname",
                "password": "admin@1234",
                "role": "user",
                "phone": "+918989535207",
            }
        }
    }


class MongoSampleRequest(BaseModel):
    email: str = EmailStr
    first_name: str = Field(min_length=5, max_length=10)
    last_name: str = Field(min_length=3, max_length=15)
    password: str
    age: int = Field(gt=10)
    address: str = Field(min_length=10, max_length=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "someemail@gmail.com",
                "first_name": "fname",
                "last_name": "lname",
                "password": "admin@1234",
                "age": 23,
                "address": "1234 Elm Street, Apt 56B, Springfield, IL 62704, United States",
            }
        }
    }
