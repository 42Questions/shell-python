from typing import Final
from .shell_command import ShellCommand, Echo, BuiltIn, PWD, CD
from .constants import Commands

COMMANDS: Final[dict[str, ShellCommand]] = {
    Commands.ECHO.value:Echo,
    Commands.TYPE.value:BuiltIn,
    Commands.PWD.value:PWD,
    Commands.CD.value:CD,
    }
