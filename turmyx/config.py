import os
from pathlib import Path
from typing import AnyStr
import abc
from configparser import ConfigParser, ExtendedInterpolation
from urllib.parse import urlparse

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = Path(__file__).parent.absolute() / "configuration.ini"


def parse_path(file: str):
    return Path(file).name.split(".")[-1]


def parse_url(url: str) -> str:
    return urlparse(url).netloc


class TurmyxConfig(abc.ABC):

    @abc.abstractmethod
    def guess_file_command(self, extension: str) -> str:
        pass

    @abc.abstractmethod
    def guess_url_command(self, domain: str) -> str:
        pass

    @abc.abstractmethod
    def load(self, config_file: Path = CONFIG_FILE) -> 'TurmyxConfig':
        pass

    @abc.abstractmethod
    def save(self, config_file: Path = CONFIG_FILE):
        pass


class CfgConfig(ConfigParser, TurmyxConfig):
    def __init__(self):
        self.__config_file_path = None
        super(CfgConfig, self).__init__(interpolation=ExtendedInterpolation())

    def load(self, config_file: Path = CONFIG_FILE) -> 'CfgConfig':
        self.__config_file_path = config_file
        self.read(config_file.as_posix())
        return self

    def save(self, config_file: Path = CONFIG_FILE):
        self.write(config_file.open("w"))

    def guess_file_command(self, extension) -> str:
        for section in self.sections():
            if "default" not in section and "editor" in section:
                if extension in self[section]["extensions"].split(" "):
                    return section

        return "editor:default"

    def guess_url_command(self, domain: str) -> str:
        for section in self.sections():
            if "default" not in section and "opener" in section:
                print(section)
                if domain in self[section]["domains"].split(" "):
                    return section

        return "opener:default"