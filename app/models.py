from enum import Enum

from pydantic import BaseModel

from constants import MAX_IMAGES


class ImagesResponseFormat(str, Enum):
    url = "url"
    b64 = "b64"


class Language(str, Enum):
    en = "en"
    it = "it"


class Sentence(BaseModel):
    text: str
    language: Language
    max_images: int = MAX_IMAGES
    response_format: ImagesResponseFormat = ImagesResponseFormat.b64


class RestrictionFilter(BaseModel):
    sex: bool
    violence: bool


class Image(BaseModel):
    data: str
    filter: RestrictionFilter


class ImagesResult(BaseModel):
    sentence_filter: RestrictionFilter
    images: list[Image]
