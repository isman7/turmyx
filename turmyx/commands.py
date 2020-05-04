from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Union, Optional
from subprocess import Popen


@dataclass(repr=False)
class Command(Popen):
    """
    A "frozen" subprocess.Popen class, with some additional fields for Turmyx.
    """
    command: str
    command_args: str = ""

    def __call__(self, uri: str, **kwargs) -> 'Command':
        args = [self.command] + self.command_args.split(" ") + [uri]
        args.remove("")
        super(Command, self).__init__(args, **kwargs)
        return self

