from pydantic import BaseModel, HttpUrl

from app.models.images import ContentClassification


class Dalle3Image(BaseModel):
    text_classification: ContentClassification
    image_classification: ContentClassification
    url: HttpUrl
