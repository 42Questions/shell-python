import os
import shlex
import sys
from typing import Final
import subprocess

from app.shell_command import ShellCommand
from app.utils import CommandKwargs, find_executable
from app.constants import Commands, ReturnCode
from app.config import COMMANDS

def execute_user_command(args: list[str], command_kwargs: CommandKwargs) -> tuple[ReturnCode, str|None]:
    try:
        if find_executable(args[0], command_kwargs.paths):
            proc = subprocess.run([args[0], *args[1:]], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
            return_code = ReturnCode.SUCCESS if proc.returncode == 0 else ReturnCode.FAILURE
            output = proc.stdout if proc.stdout else proc.stderr
            return return_code, output
        else:
            return ReturnCode.FAILURE, f"{args[0]}: command not found\n"
    except Exception as e:
        return ReturnCode.FAILURE, f"Error executing command: {e}\n"

def get_redirect_to(args: list[str]) -> tuple[list[str], str|None]:
    new_args: list[list[str]] = []
    has_redirect:bool = False
    for arg in args:
        if arg == ">" or arg == "1>":
            has_redirect = True
            break
        new_args.append(arg)
    if has_redirect:
        redirect_to = args[len(args)-1]
        return new_args, redirect_to
    return args, None

def main():
    print(os.getcwd())
    running = True
    while running:
        sys.stdout.write("$ ")
        args, redirect_to = get_redirect_to(shlex.split(input(), posix=True))
        if args[0] == Commands.EXIT.value:
            return 0
        paths: Final[list[str]] = os.getenv("PATH","").split(os.pathsep)
        command_kwargs: Final[CommandKwargs] = CommandKwargs(paths=paths)

        return_code, output = None, None
        if COMMANDS.get(args[0]):
            command: Final[ShellCommand] =COMMANDS[args[0]](args, command_kwargs)
            return_code, output = command.execute()
        else:
            return_code, output = execute_user_command(args, command_kwargs)

        if redirect_to:
            try:
                with open(redirect_to, "w") as f:
                    if output:
                        f.write(output)
            except Exception as e:
                sys.stderr.write(f"Error redirecting output to {redirect_to}: {e}\n")
        else:
            if return_code == ReturnCode.SUCCESS and output:
                sys.stdout.write(output)
            elif return_code == ReturnCode.FAILURE and output:
                sys.stderr.write(output)

if __name__ == "__main__":
    main()
