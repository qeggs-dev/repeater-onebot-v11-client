import re
import asyncio

from ...assist import escape_string
from ...command_register import CommandPackage, CommandCaller
from typing import Type, Any

pattern = re.compile(r"^(?P<command>\w+?)\s+?(?P<args>.*)$", re.IGNORECASE | re.DOTALL)

def parse_input(lines: list[str]) -> list[tuple[type[CommandPackage[Any]], str]]:
    command_call: list[tuple[Type[CommandPackage[Any]], str]] = []
    for index, line in enumerate(lines, start=1):
        matched = pattern.match(line)
        if matched:
            command = matched.group("command")
            args = matched.group("args")
            assert isinstance(command, str) and isinstance(args, str), "command and args must be str"

            try:
                package = CommandCaller.match_trigger(command)
            except KeyError as e:
                raise ValueError(f"[{index}] Command Not Found: {command}") from e

            try:
                escaped_args = escape_string(args)
            except ValueError as e:
                raise ValueError(f"[{index}] Escape Error: {e}") from e
            
            command_call.append(
                (
                    package,
                    escaped_args
                )
            )
        else:
            raise ValueError(f"[{index}] Invalid Command Format")
    return command_call