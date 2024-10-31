from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from app.config import settings

api_key_client_header = APIKeyHeader(name="api-key", auto_error=False)


def get_api_key_client(api_key_header: str = Security(api_key_client_header)):
    if api_key_header == settings.dalle3.client_apikey:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
