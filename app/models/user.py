from pydantic import BaseModel


class User(BaseModel):
    username: str
    disabled: bool = False


class UserInDB(User):
    hashed_password: str
