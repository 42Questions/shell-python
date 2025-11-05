import os
import sys
from typing import Final
import subprocess

from .shell_command import ShellCommand
from .utils import CommandKwargs, find_executable
from .constants import Commands, ReturnCode
from .config import COMMANDS

def execute_user_command(args: list[str], command_kwargs: CommandKwargs) -> ReturnCode:
    try:
        if find_executable(args[0], command_kwargs.paths):
            proc = subprocess.run([args[0], *args[1:]])
            return ReturnCode.SUCCESS if proc.returncode == 0 else ReturnCode.FAILURE
        else:
            sys.stdout.write(f"{args[0]}: command not found\n")
            return ReturnCode.FAILURE
    except Exception as e:
        sys.stdout.write(f"Error executing command: {e}\n")
        return ReturnCode.FAILURE

def main():
    running = True
    while running:
        sys.stdout.write("$ ")
        args: Final[list[str]] = input().split(" ")
        if args[0] == Commands.EXIT.value:
            return 0
        paths: Final[list[str]] = os.getenv("PATH","").split(os.pathsep)
        command_kwargs: Final[CommandKwargs] = CommandKwargs(paths=paths)

        if COMMANDS.get(args[0]):
            command: Final[ShellCommand] =COMMANDS[args[0]](args, command_kwargs)
            command.execute()
        else:
            execute_user_command(args, command_kwargs)

if __name__ == "__main__":
    main()
