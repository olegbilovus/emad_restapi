from app.utility import check_env

# Make sure it runs before importing the rest of the modules
check_env()

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.auth import Token, authenticate_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from app.models.user import User

from typing import Annotated

from fastapi import FastAPI, Query, Depends, HTTPException

from app.constants import Tags
from app.control import check_restriction_filter
from app.models.images import Sentence, ImagesResult

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.post("/token", tags=[Tags.auth])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", tags=[Tags.users])
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
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
async def create_images(current_user: Annotated[User, Depends(get_current_active_user)],
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
