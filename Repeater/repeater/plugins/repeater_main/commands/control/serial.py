import re
import asyncio

from typing import Any, Type, Coroutine
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ..._adaptation_info import __adaptation__
from ._parse_input import parse_input


@CommandCaller.register
class Serial(CommandPackage):
    cmd = "serial"
    aliases = {
        "ser",
        "SER",
        "Serial",
        "SERIAL",
    }
    cmd_type = CmdTypes.CONTROL
    documents = f"""
        Execute Commands Serially

        Usage:
            /{cmd}
            cmd1_trigger cmd1_args...
            cmd2_trigger cmd2_args...
            ...
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        command_call: list[tuple[Type[CommandPackage[Any]], str]] = await parse_input(persona_info, send_msg)
        
        tasks: list[Coroutine[Any, Any, Any]] = []
        for index, (package, args) in enumerate(command_call):
            try:
                package_instance = CommandCaller.get_instance(package)
            except KeyError:
                await send_msg.send_error(f"[{index}] Handler instance not found")
                send_msg.break_handler()
            copyed_persona_info = persona_info.copy_with_args(args)
            copyed_send_msg = send_msg.copy_with_component(
                package_instance.component
            )
            tasks.append(
                CommandCaller.horizontal_call(
                    package_instance,
                    persona_info = copyed_persona_info,
                    send_msg = copyed_send_msg
                )
            )
        
        results = [await task for task in tasks]

        buffer: list[str] = []
        for index, ((package, args), result) in enumerate(zip(command_call, results)):
            package_instance = CommandCaller.get_instance(package)
            buffer.append(
                f"[{index}] {package_instance.component} -> {result}"
            )
        
        await send_msg.send_check_length("\n".join(buffer))