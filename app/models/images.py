from enum import Enum
from typing import Annotated, List

from pydantic import BaseModel, Field, HttpUrl


class Language(str, Enum):
    en = "en"
    it = "it"


class Sentence(BaseModel):
    text: str
    language: Language


class RestrictionFilter(BaseModel):
    sex: bool
    violence: bool


class ImageURL(BaseModel):
    url: HttpUrl
    filter: RestrictionFilter


class ImagesResult(BaseModel):
    sentence_filter: RestrictionFilter
    images: List[ImageURL]
