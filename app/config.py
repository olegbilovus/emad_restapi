from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    images_url_root: HttpUrl
    core_url_it: HttpUrl
    core_url_en: HttpUrl


settings = Settings()

CORE_URLS = {
    "it": f"{settings.core_url_it}/v1/nlp/images/",
    "en": f"{settings.core_url_en}/v1/nlp/images/",
}
