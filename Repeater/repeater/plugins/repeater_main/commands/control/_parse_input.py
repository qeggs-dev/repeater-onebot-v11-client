from ...assist import escape_string
from ...command_register import CommandPackage, CommandCaller
from nonebot.adapters.onebot.v11 import Message
from typing import Type, Any

def parse_input(message: list[Message]) -> list[tuple[type[CommandPackage[Any]], Message]]:
    command_call: list[tuple[Type[CommandPackage[Any]], Message]] = []
    for index, line in enumerate(message, start=1):
        if not line:
            continue

        name: str = ""
        args: Message = Message()
        first_segment = line[0]
        if first_segment.type == "text":
            text = first_segment.data["text"]
            prefix, rest_text = split_cmd_prefix(text)
            if not prefix:
                raise ValueError(f"[{index}] {rest_text} is not a command")
            
            name_buffer: list[str] = []
            for index, char in enumerate(rest_text):
                if char == " ":
                    name = "".join(name_buffer)
                    rest_text = rest_text[index + 1:]
                    break
                name_buffer.append(char)
            
            args = Message(rest_text)
            args.extend(line[1:])
        else:
            raise ValueError(f"[{index}] first segment is not a text")

        command_call.append(
            (
                CommandCaller.match_trigger(name),
                args
            )
        )

    return command_call

def split_cmd_prefix(name: str) -> tuple[str, str]:
    for prefix in CommandCaller.cmd_prefixs():
        if name.startswith(prefix):
            return prefix, name.removeprefix(prefix)

    return "", name