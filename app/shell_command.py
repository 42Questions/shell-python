from abc import ABC, abstractmethod
from typing import Final
import os
from typing import Any
import sys

from app.utils import CommandKwargs, find_executable
from app.constants import BUILT_IN_COMMANDS, ReturnCode

class ShellCommand(ABC):
    _args: Final[list]
    _command_kwargs: Final[CommandKwargs]

    def __init__(self, args:list, command_kwargs: CommandKwargs) -> None:
        self._args = args
        self._command_kwargs = command_kwargs

    @property
    def args(self) -> list:
        return self._args
    
    @property
    def command_kwargs(self) -> CommandKwargs:
        return self._command_kwargs

    @abstractmethod
    def execute(self) -> tuple[ReturnCode, Any]:
        pass


class Echo(ShellCommand):
    def execute(self) -> ReturnCode:
        return ReturnCode.SUCCESS, " ".join(self.args[1:]) + "\n"

class BuiltIn(ShellCommand):
    def execute(self) -> ReturnCode:
        if self._args[1] in BUILT_IN_COMMANDS:
            return ReturnCode.SUCCESS, f"{self.args[1]} is a shell builtin\n"
        else:
            executable_path = find_executable(self.args[1], self.command_kwargs.paths)
            if executable_path:
                return ReturnCode.SUCCESS, f"{self.args[1]} is {executable_path}\n"
        return ReturnCode.SUCCESS, f"{self.args[1]}: not found\n"
    
class PWD(ShellCommand):
    def execute(self) -> ReturnCode:
        return ReturnCode.SUCCESS, os.getcwd() + "\n"
    
class CD(ShellCommand):
    def execute(self) -> ReturnCode:
        try:
            os.chdir(os.path.expanduser(self.args[1]) if self.args[1]=="~" else self.args[1])
        except FileNotFoundError:
            return ReturnCode.FAILURE, f"cd: {self.args[1]}: No such file or directory\n"
        return ReturnCode.SUCCESS, None

#  sys.stdout.write
# sys.stderr.write
