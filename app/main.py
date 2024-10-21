from app.utility import check_env

# Make sure it runs before importing the rest of the modules
check_env()

from pydantic import EmailStr

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth import Token, authenticate_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_user, hash_password
from app.models.user import User, UserCreate

from typing import Annotated

from fastapi import FastAPI, Query, Depends, HTTPException, Body

from app.constants import Tags
from app.control import check_restriction_filter
from app.models.images import Sentence, ImagesResult

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.post("/token", tags=[Tags.auth])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> Token:
    """
    Get an access token for a user
    - **username**: the username of the user
    - **password**: the password of the user
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@app.post("/users/", tags=[Tags.users])
async def create_user(user: UserCreate) -> User:
    """
    Create a new user
    - **username**: the username of the user
    - **email**: the email of the user
    - **password**: the password of the user
    """
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
    }
    return user


@app.patch("/users/me/", tags=[Tags.users])
async def update_user(email: Annotated[EmailStr, Body()], password: Annotated[str, Body(min_length=8)],
                      current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Update the current user
    - **email**: the new email of the user or the same email
    - **password**: the new password of the user or the same password
    """
    fake_users_db[current_user.username] = {
        "username": current_user.username,
        "email": email,
        "hashed_password": hash_password(password),
    }

    return User(username=current_user.username, email=email)


@app.delete("/users/me/", tags=[Tags.users])
async def delete_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Delete the current user
    """
    del fake_users_db[current_user.username]
    return current_user


@app.get("/users/me/", tags=[Tags.users])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Get the current user
    """
    return current_user


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    - **max_images**: the maximum number of images to return
    - **response_format**: the format of the images to return
    """
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)


# POST because the user may create new images
@app.post("/v1/images/", tags=[Tags.images], summary="Create images")
async def create_images(current_user: Annotated[User, Depends(get_current_user)],
                        sentence: Sentence) -> ImagesResult:
    """
    Create images for a sentence

    - **text**: the sentence for which to create images
    - **language**: the language of the sentence
    - **max_images**: the maximum number of images to create.
    - **response_format**: the format of the images to return
    """
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)
