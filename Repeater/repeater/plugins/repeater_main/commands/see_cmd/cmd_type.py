from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ._assists import see_cmds
from typing import Type

@CommandCaller.register
class CmdType(CommandPackage):
    cmd = "cmdType"
    aliases = {
        "ct",
        "ct",
        "cmd_type",
        "Cmd_Type",
        "CmdType",
        "CMD_TYPE"
    }
    cmd_type = CmdTypes.SEE_CMD
    documents = f"""
        View the details of the specified command.

        Usage:
        ```
        /{cmd} command
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        commands: dict[CmdTypes, list[CommandPackage]] = {}

        try:
            cmd_type = CmdTypes(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Invalid command type.")
            return

        delimiters = CommandCaller.delimiters()

        if cmd_type not in CommandCaller.types:
            await send_msg.send_error(f"\"{cmd_type}\" is not a valid command type.")
            return
        now_type_cmds: list[Type[CommandPackage]] = CommandCaller.types[cmd_type]
        commands[cmd_type] = [CommandCaller.commands[cmd] for cmd in now_type_cmds]
        
        if not now_type_cmds:
            await send_msg.send_error(f"\"{cmd_type}\" has not any commands")
        
        await see_cmds(
            commands = commands,
            delimiters = delimiters,
            send_msg = send_msg
        )