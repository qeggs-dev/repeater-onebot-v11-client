from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ._assists import (
    match_command,
    see_cmds
)
from nonebot import get_driver

@CommandCaller.register
class SeeCmd(CommandPackage):
    cmd = "seeCmd"
    aliases = {
        "sc",
        "sc",
        "see_cmd",
        "See_Cmd",
        "SeeCmd",
        "SEE_CMD"
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

        cmd_name = persona_info.message_striped_str
        config = get_driver().config
        delimiters = config.command_sep

        for package in CommandCaller.commands.values():
            if not hasattr(package, "cmd"):
                continue
            if match_command(package.cmd, cmd_name, delimiters):
                if package.cmd_type not in commands:
                    commands[package.cmd_type] = []
                if package.enabled:
                    commands[package.cmd_type].append(package)
            elif package.aliases:
                for alias in package.aliases:
                    if match_command(alias, cmd_name, delimiters):
                        if package.cmd_type not in commands:
                            commands[package.cmd_type] = []
                        if package.enabled:
                            commands[package.cmd_type].append(package)
                        break
        
        if not commands:
            await send_msg.send_error(f"\"{cmd_name}\" is Not A Valid Command")
        
        await see_cmds(
            delimiters = delimiters,
            commands = commands,
            send_msg = send_msg
        )