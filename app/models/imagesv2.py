from pydantic import Field, BaseModel

from app.models.images import ContentClassification, Language


class Sentence(ContentClassification):
    text: str
    language: Language
    one_image: bool = Field(False, description="Return only one image per keyword")


class Image(ContentClassification):
    id: int


class KeywordImages(BaseModel):
    keyword: str
    images: list[Image]
