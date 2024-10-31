from typing import Annotated

import requests
from fastapi import FastAPI, Query
from fastapi.openapi.models import APIKey
from fastapi.params import Depends

from app.auth import get_api_key_client
from app.config import settings, CORE_URLS
from app.constants import Tags
from app.models.genai import Dalle3Image
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


if settings.dalle3.valid:
    @app.get("/v1/genai/dalle3/images/", tags=[Tags.images], summary="Get images from GenAI")
    async def get_images_genai(text: str, api_key: APIKey = Depends(get_api_key_client)) -> Dalle3Image:
        """
        Get images for a sentence from GenAI
        - **text**: the sentence for which to get image
        """

        dalle3_response = requests.post(
            settings.dalle3.dalle3_endpoint,
            json={"prompt": text},
            headers={"api-key": settings.dalle3.dalle3_apikey},
        ).json()

        text_classification = ContentClassification(sex=False, violence=False)
        if dalle3_response["data"][0]["prompt_filter_results"]["sexual"]["severity"] != "safe":
            text_classification.sex = True
        if dalle3_response["data"][0]["prompt_filter_results"]["violence"]["severity"] != "safe":
            text_classification.violence = True

        image_classification = ContentClassification(sex=False, violence=False)
        if dalle3_response["data"][0]["content_filter_results"]["sexual"]["severity"] != "safe":
            image_classification.sex = True
        if dalle3_response["data"][0]["content_filter_results"]["violence"]["severity"] != "safe":
            image_classification.violence = True

        return Dalle3Image(text_classification=text_classification, image_classification=image_classification,
                           url=dalle3_response["data"][0]["url"])
