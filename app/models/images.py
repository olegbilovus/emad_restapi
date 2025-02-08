from enum import Enum
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, HttpUrl

from app.config import settings


class Language(str, Enum):
    it = "it"
    en = "en"


class ContentClassification(BaseModel):
    sex: bool = Field(False, description="Filter out sexual content")
    violence: bool = Field(False, description="Filter out violent content")


class Sentence(ContentClassification):
    text: str
    language: Language
    fix_sentence: bool = Field(settings.force_fix_sentence, description="Fix the sentence using AI")


class Image(ContentClassification):
    id: int
    keyword: str


class ImagesResult(BaseModel):
    text_classification: ContentClassification
    fixed_text: Annotated[Optional[str], Field(None)]
    url_root: HttpUrl
    images: List[Image]
