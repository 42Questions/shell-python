from typing import NamedTuple
import os

class CommandKwargs(NamedTuple):
    paths: list[str]

def check_executable(file_path: str) -> bool:
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def find_executable(command: str, paths: list[str]) -> str | None:
    for path in paths:
        full_path = os.path.join(path, command)
        if check_executable(full_path):
            return full_path
    return None

