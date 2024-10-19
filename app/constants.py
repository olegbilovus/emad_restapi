import os
from enum import Enum

MAX_IMAGES = 5 if os.getenv("MAX_IMAGES") is None else int(os.getenv("MAX_IMAGES"))


class Tags(Enum):
    images = "images"
