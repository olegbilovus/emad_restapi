from enum import Enum
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class Language(str, Enum):
    it = "it"
    en = "en"


class ContentClassification(BaseModel):
    sex: bool = Field(False, description="Filter out sexual content")
    violence: bool = Field(False, description="Filter out violent content")


class Sentence(ContentClassification):
    text: str
    language: Language


class Image(ContentClassification):
    id: int
    keyword: str


class ImagesResult(BaseModel):
    text_classification: ContentClassification
    url_root: HttpUrl
    images: List[Image]
