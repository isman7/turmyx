import os
from pathlib import Path
from typing import AnyStr
import abc
from configparser import ConfigParser, ExtendedInterpolation
from urllib.parse import urlparse

from subprocess import Popen
from .commands import Command

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = Path(__file__).parent.absolute() / "configuration.ini"


def parse_path(file: str):
    return Path(file).name.split(".")[-1]


def parse_url(url: str) -> str:
    return urlparse(url).netloc


class TurmyxConfig(abc.ABC):

    @abc.abstractmethod
    def guess_file_command(self, extension: str) -> Command:
        pass

    @abc.abstractmethod
    def guess_url_command(self, domain: str) -> Command:
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

    __map_sub_section = {
        "editor": "extensions",
        "opener": "domains"
    }

    def __get_section_name(self, extension, kind="editor") -> str:
        for section in self.sections():
            if "default" not in section and kind in section:
                if extension in self[section][self.__map_sub_section.get(kind)].split(" "):
                    return section

        return f"{kind}:default"

    def __get_command(self, section: str) -> Command:
        command = self[section]["command"]
        if "command_args" in section:
            arguments = self[section]["command_args"]
            return Command(command, command_args=arguments)
        return Command(command)

    def guess_file_command(self, extension: str) -> Command:
        section = self.__get_section_name(extension)
        return self.__get_command(section)

    def guess_url_command(self, domain: str) -> Command:
        section = self.__get_section_name(domain, kind="opener")
        return self.__get_command(section)
