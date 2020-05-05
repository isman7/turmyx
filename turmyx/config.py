from typing import List, Union
from abc import ABC, abstractmethod
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

from turmyx.commands import Command, CommandEntry

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

CONFIG_FILE = Path(__file__).parent.parent.absolute() / "turmyxconf.ini"


class TurmyxConfig(ABC):

    get_classes_name = staticmethod(dict(editor="extensions", opener="domains").get)

    @abstractmethod
    def load(self, config_file: Path = CONFIG_FILE) -> 'TurmyxConfig':
        pass

    @abstractmethod
    def save(self, config_file: Path = CONFIG_FILE):
        pass

    @abstractmethod
    def get_file_editor(self, extension: str) -> Command:
        pass

    @abstractmethod
    def get_url_opener(self, domain: str) -> Command:
        pass

    @abstractmethod
    def set_file_editor(self, command: Union[Command, CommandEntry]) -> 'TurmyxConfig':
        pass

    @abstractmethod
    def set_url_opener(self, command: Union[Command, CommandEntry]) -> 'TurmyxConfig':
        pass

    @abstractmethod
    def remove_file_editor(self, command_name: str) -> 'TurmyxConfig':
        pass

    @abstractmethod
    def remove_url_opener(self, command_name: str) -> 'TurmyxConfig':
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

    def __get_section_name(self, extension, kind="editor") -> str:
        for section in self.sections():
            if "default" not in section and kind in section:
                if extension in self[section][self.get_classes_name(kind)].split(" "):
                    return section

        return f"{kind}:default"

    def __get_command(self, section: str, kind="editor") -> Command:
        command = self[section]["command"]
        arguments = self[section]["command_args"] if "command_args" in section else ""
        classes = self[section][self.get_classes_name(kind)].split(" ")
        return Command(command, args=arguments, classes=classes, name=section.split(":")[0])

    def get_file_editor(self, extension: str) -> Command:
        section = self.__get_section_name(extension)
        return self.__get_command(section)

    def get_url_opener(self, domain: str) -> Command:
        section = self.__get_section_name(domain, kind="opener")
        return self.__get_command(section, kind="opener")

    def __set_command(self, command: Union[Command, CommandEntry], kind: str = "editor"):
        name = command.name if command.name else Path(command.command).name
        section = f"{kind}:{name}"
        if section not in self:
            self[section] = dict()
        self.set(section, "command", command.command)
        self.set(section, "command_args", command.args)
        self.set(section, self.get_classes_name(kind), " ".join(command.classes))
        return self

    def set_file_editor(self, command: Union[Command, CommandEntry]) -> 'CfgConfig':
        return self.__set_command(command)

    def set_url_opener(self, command: Union[Command, CommandEntry]) -> 'CfgConfig':
        return self.__set_command(command, kind="opener")

    def __remove_command(self, command_name: str, kind: str = "editor") -> 'CfgConfig':
        if self.remove_section(f"{kind}:{command_name}"):
            return self
        else:
            raise ValueError("Command not found in config file.")

    def remove_file_editor(self, command_name: str) -> 'CfgConfig':
        return self.__remove_command(command_name)

    def remove_url_opener(self, command_name: str) -> 'CfgConfig':
        return self.__remove_command(command_name, kind="opener")
