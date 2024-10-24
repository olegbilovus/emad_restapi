from typing import Annotated

from fastapi import FastAPI, Query

from app.config import settings
from app.constants import Tags
from app.models.images import Sentence, ImagesResult, ContentClassification, Image

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **sex**: display sexual content
    - **violence**: display violent content
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    """
    text_classification = ContentClassification()
    images = [Image(id=2239, content_classification=text_classification),
              Image(id=15475, content_classification=text_classification)]

    return ImagesResult(text_classification=text_classification, url_root=settings.images_url_root, images=images)
