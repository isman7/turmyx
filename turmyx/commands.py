from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Union, Optional, Dict
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

    @classmethod
    def from_command(cls, command: CommandEntry):
        return cls(**asdict(command))


# TODO use CommandDict only for editors or openers...
class CommandDict(dict):

    def __init__(self, cfg: Dict[str, Dict[str, dict]]):
        self.default = CommandEntry(name="default", **cfg.get("default"))
        editors = cfg.get("commands")
        super(CommandDict, self).__init__((n, CommandEntry(name=n, **d)) for n, d in editors.items())

        # default_opener = cfg.get("url-openers").get("default")

    def __getitem__(self, item: str) -> CommandEntry:
        super(CommandDict, self).__getitem__(item)

    def __repr__(self):
        return f"""
        {super(CommandDict, self).__repr__()}
        default: {self.default.command}
        """
