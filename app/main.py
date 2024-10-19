from typing import Annotated

from fastapi import FastAPI, Query

from constants import Tags
from control import check_restriction_filter
from models import Sentence, ImagesResult

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    - **max_images**: the maximum number of images to return
    - **response_format**: the format of the images to return
    """
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)


# POST because the user may create new images
@app.post("/v1/images/", tags=[Tags.images], summary="Create images")
async def create_images(sentence: Sentence) -> ImagesResult:
    """
    Create images for a sentence

    - **text**: the sentence for which to create images
    - **language**: the language of the sentence
    - **max_images**: the maximum number of images to create.
    - **response_format**: the format of the images to return
    """
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)
