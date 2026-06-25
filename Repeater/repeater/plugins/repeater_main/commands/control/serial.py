from typing import Any, Type, Coroutine
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
        lines = split_by_indent(persona_info.message_striped_str)
        command_call: list[tuple[Type[CommandPackage[Any]], str]] = await parse_input(lines, send_msg)
        
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
        for package, persona_info, send_msg in tasks:
            msg =  persona_info.message_striped_str
            if "$ret" in msg:
                copyed_persona_info = persona_info.copy_with_args(
                    msg.replace("$ret", str(last_result))
                )
            result = await CommandCaller.horizontal_call(
                package,
                copyed_persona_info,
                send_msg
            )
            results.append(result)
            last_result = result

        if not results:
            buffer: list[str] = []
            for index, ((package, args), result) in enumerate(zip(command_call, results)):
                package_instance = CommandCaller.get_instance(package)
                buffer.append(
                    f"[{index}] {package_instance.component} -> {result}"
                )
            
            await send_msg.send_check_length_prompt("\n".join(buffer))
        else:
            await send_msg.send_error("No Results...")