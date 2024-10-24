from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    images_url_root: HttpUrl


settings = Settings()
