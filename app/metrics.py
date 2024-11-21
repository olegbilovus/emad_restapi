import time
from abc import ABC, abstractmethod

import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.models.images import Image


class Metrics(ABC):

    @abstractmethod
    def send_metrics_perf(self, url_path, latency):
        pass

    @abstractmethod
    def send_metrics_image(self, images: list[Image], language: str, filter_sex: bool, filter_violence: bool,
                           latency: float):
        pass


class PointGenerator:
    _tag_language = "language"

    @staticmethod
    def point_perf(env, url_path, latency) -> Point:
        return Point("perf").tag("env", env).tag("path", url_path).field("latency", latency).time(time.time_ns())

    @staticmethod
    def points_image(env, images: list[Image], language: str, filter_sex: bool, filter_violence: bool,
                     latency: float) -> list[Point]:
        points = []
        now_ns = time.time_ns()
        for i, image in enumerate(images, start=1):
            point_kw = (Point("keyword").tag("env", env).tag(PointGenerator._tag_language, language)
                        .field("keyword", image.keyword)
                        .field("sex", image.sex)
                        .field("violence", image.violence)
                        .field("found", image.id != -1)
                        .time(now_ns + i * 10000))
            points.append(point_kw)

        point_stats = (Point("stats").tag("env", env).tag(PointGenerator._tag_language, language)
                       .field("num_kw", len(images))
                       .field("latency", latency)
                       .field("filter_sex", filter_sex)
                       .field("filter_violence", filter_violence))
        point_stats.time(now_ns)
        points.append(point_stats)

        return points


class InfluxDB(Metrics):

    def __init__(self, url, token, org, bucket, verify_ssl=True, env="dev"):
        self._client = InfluxDBClient(url, token, org, verify_ssl=verify_ssl)

        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
        self._bucket = bucket
        self._org = org

        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()

        self._env = env

    def _write(self, *points: Point):
        self._write_api.write(self._bucket, self._org, points, write_precision=WritePrecision.NS)

    def send_metrics_perf(self, url_path, latency):
        point = PointGenerator.point_perf(self._env, url_path, latency)
        self._write(point)

    def send_metrics_image(self, images: list[Image], language: str, filter_sex: bool, filter_violence: bool,
                           latency: float):
        points = PointGenerator.points_image(self._env, images, language, filter_sex, filter_violence, latency)
        self._write(*points)


class Prometheus(Metrics):

    def __init__(self, url, user, password, env="dev"):
        self._url = url
        self._env = env

        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "text/plain", "Authorization": f"Bearer {user}:{password}"})

    def _write(self, *points: Point):
        line_protocol = ""
        for point in points:
            line_protocol += point.to_line_protocol() + "\n"

        self._session.post(self._url, data=line_protocol)

    def send_metrics_perf(self, url_path, latency):
        point = PointGenerator.point_perf(self._env, url_path, latency)
        self._write(point)

    def send_metrics_image(self, images: list[Image], language: str, filter_sex: bool, filter_violence: bool,
                           latency: float):
        points = PointGenerator.points_image(self._env, images, language, filter_sex, filter_violence, latency)
        self._write(*points)
