from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str
    email: EmailStr


class UserCreate(User):
    password: Annotated[str, Field(min_length=8)]


class UserInDB(User):
    hashed_password: str
