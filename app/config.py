from pydantic import HttpUrl
from pydantic_settings import BaseSettings

_EXAMPLE_URL = "https://example.home.arpa"


class Dalle3GenAISettings(BaseSettings):
    dalle3_endpoint: HttpUrl = HttpUrl(_EXAMPLE_URL)
    dalle3_apikey: str = ""
    client_apikey: str = ""  # This is the API key for the client


class InfluxDB(BaseSettings):
    influxdb_org: str = ""
    influxdb_url: HttpUrl = HttpUrl(_EXAMPLE_URL)
    influxdb_token: str = ""
    influxdb_bucket: str = ""
    influxdb_verify_ssl: bool = True


class Prometheus(BaseSettings):
    prometheus_url: HttpUrl = HttpUrl(_EXAMPLE_URL)
    prometheus_user: str = ""
    prometheus_password: str = ""


class OpenAI(BaseSettings):
    openai_base_url: str = _EXAMPLE_URL
    openai_api_key: str = ""
    openai_model: str = ""


class GoogleAI(BaseSettings):
    googleai_api_key: str = ""
    googleai_model: str = ""


class Settings(BaseSettings):
    app_env: str = "dev"
    images_url_root: HttpUrl
    core_url_it: HttpUrl
    core_url_en: HttpUrl
    dalle3: Dalle3GenAISettings = Dalle3GenAISettings()
    cors_origins: str = "*"
    influxdb: InfluxDB = InfluxDB()
    prometheus: Prometheus = Prometheus()
    openai: OpenAI = OpenAI()
    googleai: GoogleAI = GoogleAI()
    force_fix_sentence: bool = False


settings = Settings()

CORE_URLS = {
    "it": f"{settings.core_url_it}/v1/nlp/images/",
    "en": f"{settings.core_url_en}/v1/nlp/images/",
}


def is_dalle3_valid():
    return (
        settings.dalle3.dalle3_endpoint != _EXAMPLE_URL and
        settings.dalle3.dalle3_apikey != "" and
        settings.dalle3.client_apikey != ""
    )


def is_influxdb_valid():
    return (
        settings.influxdb.influxdb_org != "" and
        settings.influxdb.influxdb_url != _EXAMPLE_URL and
        settings.influxdb.influxdb_token != "" and
        settings.influxdb.influxdb_bucket != ""
    )


def is_prometheus_valid():
    return (
        settings.prometheus.prometheus_url != _EXAMPLE_URL and
        settings.prometheus.prometheus_user != "" and
        settings.prometheus.prometheus_password != ""
    )


def is_openai_valid():
    return (
        settings.openai.openai_base_url != _EXAMPLE_URL and
        settings.openai.openai_api_key != "" and
        settings.openai.openai_model != ""
    )


def is_googleai_valid():
    return (
        settings.googleai.googleai_api_key != "" and
        settings.googleai.googleai_model != ""
    )
