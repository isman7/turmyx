from pathlib import Path
from dataclasses import dataclass
from typing import List, Union
import subprocess


@dataclass(frozen=True, repr=False)
class Command(subprocess.Popen):
    """
    A frozen subprocess.Popen class, with some abstract API for Turmyx.
    """
    command: str
    command_args: List

    def __call__(self, uri: str, **kwargs):
        args = [self.command] + self.command_args.split(" ") + [uri]
        super(Command, self).__init__(*args, **kwargs)
        return self.communicate()
