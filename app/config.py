from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Dalle3GenAISettings(BaseSettings):
    dalle3_endpoint: HttpUrl = HttpUrl("https://example.home.arpa")
    dalle3_apikey: str = ""
    client_apikey: str = ""  # This is the API key for the client
    valid: bool = False


class Settings(BaseSettings):
    images_url_root: HttpUrl
    core_url_it: HttpUrl
    core_url_en: HttpUrl
    dalle3: Dalle3GenAISettings = Dalle3GenAISettings()


settings = Settings()

CORE_URLS = {
    "it": f"{settings.core_url_it}/v1/nlp/images/",
    "en": f"{settings.core_url_en}/v1/nlp/images/",
}

settings.dalle3.valid = (settings.dalle3.dalle3_endpoint != "https://example.home.arpa" and
                         settings.dalle3.dalle3_apikey != "" and
                         settings.dalle3.client_apikey != "")
