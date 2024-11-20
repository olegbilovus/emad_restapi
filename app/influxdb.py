import time

import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.models.images import Image


class InfluxDB:
    _tag_language = "language"

    def __init__(self, url, token, org, bucket, verify_ssl=True):
        self._client = InfluxDBClient(url, token, org, verify_ssl=verify_ssl)

        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._bucket = bucket
        self._org = org

        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()

    def _write(self, *points: Point):
        self._write_api.write(self._bucket, self._org, points, write_precision=WritePrecision.NS)

    def send_metrics_perf(self, url_path, latency):
        point = (Point("perf").tag("path", url_path)
                 .field("latency", latency)
                 .time(time.time_ns()))

        self._write(point)

    def send_metrics_image(self, images: list[Image], language: str, filter_sex: bool, filter_violence: bool,
                           latency: float):
        points = []
        now_ns = time.time_ns()
        for i, image in enumerate(images, start=1):
            point_kw = (Point("keyword").tag(self._tag_language, language)
                        .field("keyword", image.keyword)
                        .field("sex", image.sex)
                        .field("violence", image.violence)
                        .field("found", image.id != -1)
                        .time(now_ns + i))
            points.append(point_kw)

        point_stats = (Point("stats").tag(self._tag_language, language)
                       .field("num_kw", len(images))
                       .field("latency", latency)
                       .field("filter_sex", filter_sex)
                       .field("filter_violence", filter_violence))
        point_stats.time(now_ns)
        points.append(point_stats)

        self._write(*points)
