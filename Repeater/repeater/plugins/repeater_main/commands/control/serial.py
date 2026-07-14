from typing import Any, Type, Coroutine
from nonebot.adapters.onebot.v11 import Message
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ..._adaptation_info import __adaptation__
from ._parse_input import parse_input
from ._split_by_indent import split_by_indent

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
        lines = split_by_indent(persona_info.message)
        try:
            command_call: list[tuple[Type[CommandPackage[Any]], Message]] = parse_input(lines)
        except ValueError as e:
            await send_msg.send_error(f"Invalid Input Format: {e}")
        except KeyError as e:
            await send_msg.send_error(f"Unknown Command: {e}")
        
        tasks: list[tuple[CommandPackage[Any], PersonaInfo, SendMsg]] = []
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
                (
                    package_instance,
                    copyed_persona_info,
                    copyed_send_msg
                )
            )
        
        results = []
        last_result: Any = None
        for package, info, send_msg in tasks:
            msg =  info.message_striped_str
            if "$ret" in msg:
                copyed_persona_info = info.copy_with_args(
                    msg.replace("$ret", str(last_result))
                )
            else:
                copyed_persona_info = info
            result = await CommandCaller.horizontal_call(
                package,
                copyed_persona_info,
                send_msg
            )
            results.append(result)
            last_result = result