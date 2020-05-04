from pathlib import Path
from urllib.parse import urlparse


def parse_path(file: str):
    return Path(file).name.split(".")[-1]


def parse_url(url: str) -> str:
    return urlparse(url).netloc