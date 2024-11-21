import time
from typing import Annotated

import requests
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey
from fastapi.params import Depends

from app.auth import get_api_key_client
from app.config import settings, CORE_URLS, is_dalle3_valid, is_influxdb_valid, is_prometheus_valid
from app.constants import Tags
from app.metrics import InfluxDB, Metrics, Prometheus
from app.models.genai import Dalle3Image
from app.models.images import Sentence, ImagesResult, ContentClassification, Image
from app.utils import JSONLogger

logger = JSONLogger(__name__, settings.app_env)
app = FastAPI(docs_url="/", title="AAC API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prometheus_on = is_prometheus_valid()
influxdb_on = is_influxdb_valid()
metrics_on = prometheus_on or influxdb_on
logger.info(metrics_on=metrics_on, prometheus_on=prometheus_on, influxdb_on=influxdb_on)
if metrics_on:
    if prometheus_on:
        metrics: Metrics = Prometheus(str(settings.prometheus.prometheus_url),
                                      settings.prometheus.prometheus_user,
                                      settings.prometheus.prometheus_password,
                                      env=settings.app_env)
    else:
        metrics: Metrics = InfluxDB(str(settings.influxdb.influxdb_url),
                                    settings.influxdb.influxdb_token,
                                    settings.influxdb.influxdb_org,
                                    settings.influxdb.influxdb_bucket,
                                    settings.influxdb.influxdb_verify_ssl,
                                    env=settings.app_env)

dalle3_on = is_dalle3_valid()
logger.info(dalle3_on=dalle3_on)


@app.middleware("http")
async def perf(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(uri=request.url.path, latency=process_time, status_code=response.status_code)

    if metrics_on:
        try:
            metrics.send_metrics_perf(request.url.path, process_time, response.status_code)
        except Exception as e:
            logger.error(error=str(e))

    return response


@app.get("/v1/images/", tags=[Tags.images], summary="Get images")
async def get_images(sentence: Annotated[Sentence, Query()]) -> ImagesResult:
    """
    Get already existing images for a sentence
    - **sex**: filter out sexual content
    - **violence**: filter out violent content
    - **text**: the sentence for which to get images
    - **language**: the language of the sentence
    """

    time_before = time.perf_counter()
    try:
        core_response = requests.get(CORE_URLS[sentence.language.name], params=sentence.model_dump(), timeout=3).json()
    except Exception as e:
        logger.error(error=str(e))
        raise HTTPException(status_code=500, detail="Core service is down")
    latency = round(time.perf_counter() - time_before, 3)

    images = [Image(**image) for image in core_response]

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

    return ImagesResult(text_classification=text_classification, url_root=settings.images_url_root, images=images)


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
