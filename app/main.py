from fastapi import FastAPI

from constants import MAX_IMAGES
from control import check_restriction_filter
from models import Sentence, ImagesResult, Language, ImagesResponseFormat

app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")


@app.get("/v1/images/")
async def get_images(text: str, language: Language, max_images: int = MAX_IMAGES,
                     response_format: ImagesResponseFormat = ImagesResponseFormat.b64) -> ImagesResult:
    sentence_filter = check_restriction_filter(text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)


# POST because the user may create new images
@app.post("/v1/images/")
async def create_images(sentence: Sentence) -> ImagesResult:
    sentence_filter = check_restriction_filter(sentence.text)
    images = []

    return ImagesResult(sentence_filter=sentence_filter, images=images)
