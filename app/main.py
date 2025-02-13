import time
from typing import Annotated

import requests
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey
from fastapi.params import Depends

from app.auth import get_api_key_client
from app.config import settings, CORE_URLS, is_dalle3_valid, is_influxdb_valid, is_openai_valid, is_googleai_valid
from app.constants import Tags
from app.fix_sentence import FixSentenceOpenAI, FixSentence, FixSentenceGoogle
from app.metrics import InfluxDB, Metrics
from app.models.genai import Dalle3Image
from app.models.images import Sentence, ImagesResult, ContentClassification, Image
from app.models.imagesv2 import Sentence as SentenceV2, KeywordImages, KeywordImagesResult
from app.utils import JSONLogger

logger = JSONLogger(settings.app_env)
app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_on = is_influxdb_valid()
logger.info(metrics_on=metrics_on)
if metrics_on:
    metrics: Metrics = InfluxDB(str(settings.influxdb.influxdb_url),
                                settings.influxdb.influxdb_token,
                                settings.influxdb.influxdb_org,
                                settings.influxdb.influxdb_bucket,
                                settings.influxdb.influxdb_verify_ssl,
                                env=settings.app_env)

dalle3_on = is_dalle3_valid()
logger.info(dalle3_on=dalle3_on)

openai_on = is_openai_valid()
googleai_on = is_googleai_valid()
logger.info(openai_on=openai_on)
logger.info(googleai_on=googleai_on)
global fix_sentence
openai_fix_sentence: FixSentenceOpenAI = None
google_fix_sentence: FixSentenceGoogle = None

if openai_on:
    openai_fix_sentence = FixSentenceOpenAI(settings.openai.openai_base_url, settings.openai.openai_api_key,
                                            settings.openai.openai_model)
if googleai_on:
    google_fix_sentence = FixSentenceGoogle(settings.googleai.googleai_api_key, settings.googleai.googleai_model)

fix_sentence = google_fix_sentence if googleai_on else openai_fix_sentence
logger.info(fix_sentence=fix_sentence.__class__.__name__.removeprefix(FixSentence.__name__))


@app.middleware("http")
async def perf(request: Request, call_next):
    if request.url.path == "/health":
        return await call_next(request)

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(uri=request.url.path, query=request.url.query, latency=process_time, status_code=response.status_code)

    if metrics_on:
        try:
            metrics.send_metrics_perf(request.url.path, process_time, response.status_code)
        except Exception as e:
            logger.error(error=str(e))

    return response


@app.get("/health", tags=["health"], summary="Health check", include_in_schema=False)
async def health_check():
    return {"status": "healthy"}


# noinspection t
@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **sex**: filter out sexual content
    - **violence**: filter out violent content
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    - **fix_sentence**: fix the sentence using AI
    """

    time_before = time.perf_counter()

    global fix_sentence
    if fix_sentence and (sentence.fix_sentence or settings.force_fix_sentence):
        removed_interrogative = False
        if sentence.text[-1] == "?":
            sentence.text = sentence.text[:-1]
            removed_interrogative = True
        try:
            sentence.text = fix_sentence.fix(sentence.text, sentence.language)
        except Exception as e:
            logger.error(error=str(e))
            if isinstance(fix_sentence, FixSentenceOpenAI):
                fix_sentence = google_fix_sentence
            else:
                fix_sentence = openai_fix_sentence
            logger.warn(msg="Changed AI engine",
                        fix_sentence=fix_sentence.__class__.__name__.removeprefix(FixSentence.__name__))

            try:
                sentence.text = fix_sentence.fix(sentence.text, sentence.language)
            except Exception as e:
                logger.error(error=str(e))
                raise HTTPException(status_code=500, detail="AI service to fix sentence is down")
        if removed_interrogative:
            sentence.text += "?"

    try:
        core_response = requests.get(CORE_URLS[sentence.language.name], params=sentence.model_dump(), timeout=3).json()
    except Exception as e:
        logger.error(error=str(e))
        raise HTTPException(status_code=500, detail="Core service is down")
    latency = round(time.perf_counter() - time_before, 3)

    images = []
    for keyword in core_response:
        if not keyword["images"]:
            images.append(Image(keyword=keyword["keyword"], id=-1))
        else:
            image = keyword["images"][0]
            images.append(
                Image(keyword=keyword["keyword"], id=image["id"], sex=image["sex"], violence=image["violence"]))

    logger.info(latency=latency, language=sentence.language.name, num_kw=len(images))

    text_classification = ContentClassification(sex=False, violence=False)
    for image in images:
        if image.sex:
            text_classification.sex = True
        if image.violence:
            text_classification.violence = True

    if metrics_on:
        try:
            metrics.send_metrics_image(images, sentence.language.name, sentence.sex, sentence.violence, latency)
        except Exception as e:
            logger.error(error=str(e))

    return ImagesResult(text_classification=text_classification,
                        fixed_text=sentence.text if (sentence.fix_sentence or settings.force_fix_sentence) else None,
                        url_root=settings.images_url_root, images=images)


@app.get("/v2/images/", tags=[Tags.images], summary="Get all the images for each keyword in the sentence")
async def get_all_keyword_images(sentence: Annotated[SentenceV2, Query()]) -> KeywordImagesResult:
    """
    Get all the images for each  keyword in the sentence
    - **sex**: filter out sexual content
    - **violence**: filter out violent content
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    - **one_image**: return only one image per keyword
    """

    time_before = time.perf_counter()
    try:
        core_response = requests.get(CORE_URLS[sentence.language.name], params=sentence.model_dump(), timeout=3).json()
    except Exception as e:
        logger.error(error=str(e))
        raise HTTPException(status_code=500, detail="Core service is down")
    latency = round(time.perf_counter() - time_before, 3)

    keyword_images = [KeywordImages(**keyword) for keyword in core_response]

    logger.info(latency=latency, language=sentence.language.name, num_kw=len(keyword_images))

    if metrics_on:
        try:
            metrics.send_metrics_image_v2(keyword_images, sentence.language.name, sentence.sex, sentence.violence,
                                          latency)
        except Exception as e:
            logger.error(error=str(e))

    return KeywordImagesResult(url_root=settings.images_url_root, keyword_images=keyword_images)


if dalle3_on:
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
