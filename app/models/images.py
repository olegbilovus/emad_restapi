from enum import Enum
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class Language(str, Enum):
    it = "it"


class ContentClassification(BaseModel):
    sex: bool = Field(True, description="Sexual content")
    violence: bool = Field(True, description="Violent content")


class Sentence(ContentClassification):
    text: str
    language: Language


class Image(BaseModel):
    id: int
    content_classification: ContentClassification


class ImagesResult(BaseModel):
    text_classification: ContentClassification
    url_root: HttpUrl
    images: List[Image]
