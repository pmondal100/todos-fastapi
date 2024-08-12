import uuid
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey

class Users(Base):

    __tablename__ = 'users'

    user_id: UUID = Column(UUID, primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    email: str = Column(String, unique=True)
    username: str = Column(String, unique=True)
    first_name: str = Column(String)
    last_name: str = Column(String)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    role: str = Column(String)
    phone_number: str = Column(String)

class Todos(Base):

    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(UUID, ForeignKey("users.user_id"))