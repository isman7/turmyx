from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Union, Optional
from subprocess import Popen
import shutil


@dataclass
class CommandEntry:
    command: str
    classes: List[str] = field(default_factory=list)
    args: str = ""
    name: str = ""

    def __post_init__(self):
        self.command = shutil.which(self.command)
        try:
            assert self.command
        except AssertionError:
            raise FileNotFoundError("Given command or script not found or not executable.")


class Command(CommandEntry, Popen):
    """
    A "frozen" subprocess.Popen class, with some additional fields for Turmyx.
    """

    def __call__(self, uri: str, **kwargs) -> 'Command':
        args = [self.command] + self.args.split(" ") + [uri]
        args.remove("")
        Popen.__init__(self, args, **kwargs)
        return self

