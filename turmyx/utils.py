from pathlib import Path
from urllib.parse import urlparse


def parse_path(file_path: str) -> str:
    return Path(file_path).name.split(".")[-1].lower()


def parse_url(url: str) -> str:
    return urlparse(url).netloc


def parse_uri(uri: str) -> str:
    if urlparse(uri).scheme in ('http', 'https',):
        return "url"
    else:
        return "file"
