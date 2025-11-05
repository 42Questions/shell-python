from abc import ABC, abstractmethod
from typing import Final
import os
import sys

from .utils import CommandKwargs, find_executable
from .constants import BUILT_IN_COMMANDS, ReturnCode

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
    def execute(self) -> ReturnCode:
        pass


class Echo(ShellCommand):
    def execute(self) -> ReturnCode:
        sys.stdout.write(" ".join(self.args[1:]) + "\n")
        return ReturnCode.SUCCESS

class BuiltIn(ShellCommand):
    def execute(self) -> ReturnCode:
        if self._args[1] in BUILT_IN_COMMANDS:
            sys.stdout.write(f"{self.args[1]} is a shell builtin\n")
            return ReturnCode.SUCCESS
        else:
            executable_path = find_executable(self.args[1], self.command_kwargs.paths)
            if executable_path:
                sys.stdout.write(f"{self.args[1]} is {executable_path}\n")
                return ReturnCode.SUCCESS
        sys.stdout.write(f"{self.args[1]}: not found\n")
        return ReturnCode.SUCCESS
    
class PWD(ShellCommand):
    def execute(self) -> ReturnCode:
        sys.stdout.write(os.getcwd() + "\n")
        return ReturnCode.SUCCESS
    
class CD(ShellCommand):
    pass
