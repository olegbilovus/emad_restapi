from enum import Enum
from typing import Annotated, List, Union

from pydantic import BaseModel, Field, HttpUrl

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
    max_images: Annotated[
        int, Field(le=MAX_IMAGES, description="An upper bound for the number of images to return")] = MAX_IMAGES
    response_format: ImagesResponseFormat = ImagesResponseFormat.b64


class RestrictionFilter(BaseModel):
    sex: bool
    violence: bool


class ImageB64(BaseModel):
    b64: str
    filter: RestrictionFilter


class ImageURL(BaseModel):
    url: HttpUrl
    filter: RestrictionFilter


class ImagesResult(BaseModel):
    sentence_filter: RestrictionFilter
    images: Union[List[ImageB64] | List[ImageURL]]
