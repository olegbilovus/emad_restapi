from typing import Annotated

from fastapi import FastAPI, Query

from app.constants import Tags
from app.control import check_restriction_filter
from app.models.images import Sentence, ImagesResult

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    """
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)
