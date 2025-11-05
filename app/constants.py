from enum import Enum, StrEnum
from typing import Final

class Commands(StrEnum):
    ECHO = "echo"
    TYPE = "type"
    PWD = "pwd"
    EXIT = "exit"
    CD = "cd"

BUILT_IN_COMMANDS: Final[set[str]] = {
    Commands.ECHO.value,
    Commands.EXIT.value,
    Commands.TYPE.value,
    Commands.PWD.value,
    Commands.CD.value,
    }

class ReturnCode(Enum):
    SUCCESS = 0
    FAILURE = 1