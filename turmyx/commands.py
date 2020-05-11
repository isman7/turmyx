import shutil
from dataclasses import dataclass, field, asdict
from subprocess import Popen
from typing import List, Union, Dict, Any, Optional

CommandDictType = Dict[str, Dict[str, Union[str, Dict[str, Any]]]]


@dataclass
class CommandEntry:
    command: str
    classes: Union[List[str], str] = field(default_factory=list)
    args: str = ""
    name: str = ""

    def __post_init__(self):
        self.command = shutil.which(self.command)
        try:
            assert self.command
        except AssertionError:
            raise FileNotFoundError("Given command or script not found or not executable.")

        if isinstance(self.classes, str):
            self.classes = self.classes.split(" ")

    def as_dict(self) -> Dict[str, str]:
        d = asdict(self)
        d["classes"] = " ".join(d.get("classes"))
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


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
        return cls.from_dict(command.as_dict())


class CommandDict(dict):

    def __init__(self, input_dict: Dict[str, Dict[str, dict]], default: str = "default"):

        if default not in input_dict:
            raise KeyError("default item is not found in input dict")

        super(CommandDict, self).__init__(input_dict)

        for k, v in self.items():
            self[k] = v  # Re-assign to ensure cast

        if default != "default":
            self["default"] = self.pop(default)

    @property
    def default(self):
        return self["default"]

    def __getitem__(self, item: str) -> 'CommandEntry':
        if item not in self:
            return self.default
        return super(CommandDict, self).__getitem__(item)

    def __setitem__(self, key, value):
        if not isinstance(value, CommandEntry):
            value = CommandEntry(**value)
        super(CommandDict, self).__setitem__(key, value)

    def get(self, k) -> 'CommandEntry':
        return super(CommandDict, self).get(k, self.default)

    def pop(self, k) -> 'CommandEntry':
        return super(CommandDict, self).pop(k, self.default)

    def __repr__(self):
        self_commands = "\n\t".join(f"{n}: {c}" for n, c in self.items())
        return f"""
List of commands:
    {self_commands}
"""

    def as_dict(self) -> 'CommandDictType':
        d = dict(self)
        for name, command in d.items():
            d[name] = command.as_dict()
            d[name].pop("name")
        default = d.pop("default")
        default.pop("classes")
        return dict(default=default, commands=d)

