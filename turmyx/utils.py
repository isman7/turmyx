from pathlib import Path
from urllib.parse import urlparse


def parse_extension(file: str) -> str:
    return Path(file).name.split(".")[-1].lower()


def parse_domain(url: str) -> str:
    return urlparse(url).netloc