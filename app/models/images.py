from enum import Enum
from typing import Annotated, List

from pydantic import BaseModel, Field, HttpUrl

from app.models.constants import MAX_IMAGES


class Language(str, Enum):
    en = "en"
    it = "it"


class Sentence(BaseModel):
    text: str
    language: Language
    max_images: Annotated[
        int, Field(le=MAX_IMAGES, description="An upper bound for the number of images to return")] = MAX_IMAGES


class RestrictionFilter(BaseModel):
    sex: bool
    violence: bool


class ImageURL(BaseModel):
    url: HttpUrl
    filter: RestrictionFilter


class ImagesResult(BaseModel):
    sentence_filter: RestrictionFilter
    images: List[ImageURL]
