from typing import Annotated

import requests
from fastapi import FastAPI, Query

from app.config import settings, CORE_URLS
from app.constants import Tags
from app.models.images import Sentence, ImagesResult, ContentClassification, Image

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **sex**: filter out sexual content
    - **violence**: filter out violent content
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    """

    core_response = requests.get(CORE_URLS[sentence.language.name], params=sentence.model_dump(), timeout=3).json()
    images = [Image(**image) for image in core_response]

    text_classification = ContentClassification(sex=False, violence=False)
    for image in images:
        if image.sex:
            text_classification.sex = True
        if image.violence:
            text_classification.violence = True

    return ImagesResult(text_classification=text_classification, url_root=settings.images_url_root, images=images)
