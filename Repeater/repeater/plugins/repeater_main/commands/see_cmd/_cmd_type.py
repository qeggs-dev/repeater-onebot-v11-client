from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg, CmdTypes
from ._assists import see_cmds
from nonebot import get_driver

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

        config = get_driver().config
        delimiters = config.command_sep

        now_type_cmds: list[CommandPackage] = []
        commands[cmd_type] = now_type_cmds
        for package in CommandCaller.commands.values():
            if package.cmd_type == cmd_type:
                now_type_cmds.append(package)
        
        if not now_type_cmds:
            await send_msg.send_error(f"\"{cmd_type}\" has not any commands")
        
        await see_cmds(
            commands = commands,
            delimiters = delimiters,
            send_msg = send_msg
        )