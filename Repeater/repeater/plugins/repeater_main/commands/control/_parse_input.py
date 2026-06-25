import re
import asyncio

from ...assist import PersonaInfo, SendMsg, escape_string
from ...command_register import CommandPackage, CommandCaller
from typing import Type, Any

pattern = re.compile(r"^(?P<command>\w+)\s+(?P<args>.+)$", re.IGNORECASE | re.DOTALL | re.UNICODE)

async def parse_input(persona_info: PersonaInfo, send_msg: SendMsg) -> list[tuple[type[CommandPackage[Any]], str]]:
    lines = persona_info.message_striped_str.splitlines()

    command_call: list[tuple[Type[CommandPackage[Any]], str]] = []
    for index, line in enumerate(lines, start=1):
        matched = pattern.match(line)
        if matched:
            command = matched.group("command")
            args = matched.group("args")
            assert isinstance(command, str) and isinstance(args, str), "command and args must be str"

            try:
                package = CommandCaller.triggers[command]
            except KeyError:
                await send_msg.send_error(f"[{index}] Command Not Found: {command}")
                send_msg.break_handler()

            try:
                escaped_args = escape_string(args)
            except ValueError as e:
                await send_msg.send_error(f"[{index}] Escape Error: {e}")
                send_msg.break_handler()
            
            command_call.append(
                (
                    package,
                    escaped_args
                )
            )
        else:
            await send_msg.send_error(f"[{index}] Invalid Command Format")
            send_msg.break_handler()
    return command_call