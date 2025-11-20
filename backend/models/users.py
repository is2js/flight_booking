import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserInDB(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    # hashed_password: str
    password: str
