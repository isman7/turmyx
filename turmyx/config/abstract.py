from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Optional

from turmyx.commands import Command, CommandEntry, CommandDict


CONFIG_FILE = Path(__file__).parent.parent.parent.absolute() / "turmyxconf.yml"


class TurmyxConfig(ABC):

    def __init__(self, config_file: Optional[Path] = CONFIG_FILE):
        self.config_file = config_file

    @abstractmethod
    def load(self, config_file: Optional[Path] = None) -> 'TurmyxConfig':
        pass

    @abstractmethod
    def save(self, config_file: Path):
        pass

    @abstractmethod
    def get_file_editor(self, extension: str) -> Command:
        pass

    @abstractmethod
    def get_url_opener(self, domain: str) -> Command:
        pass

    @abstractmethod
    def get_editors(self) -> CommandDict:
        pass

    @abstractmethod
    def get_openers(self) -> CommandDict:
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
