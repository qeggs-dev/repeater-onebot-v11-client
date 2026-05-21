from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ...assist import PersonaInfo, SendMsg
from typing import Iterable
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
    cmd_type = CmdType.SEE_CMD
    documents = f"""
        View the details of the specified command.

        Usage:
        ```
        /{cmd} command
        ```
    """
    
    @classmethod
    def match_command(cls, cmd: str | tuple[str, ...], cmd_name: str, delimiters: Iterable[str]):
        if isinstance(cmd, str) and cmd_name == cmd:
            return True
        elif (
            isinstance(cmd, tuple) and
            cmd_name in cls.all_joined_commands(cmd, delimiters)
        ):
            return True
        else:
            return False
    
    @staticmethod
    def all_joined_commands(cmd: tuple[str, ...], delimiters: Iterable[str]) -> set[str]:
        return {delimiter.join(cmd) for delimiter in delimiters}

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        commands: dict[CmdType, list[CommandPackage]] = {}

        cmd_name = persona_info.message_striped_str
        config = get_driver().config
        delimiters = config.command_sep

        for package in CommandCaller.commands.values():
            if not hasattr(package, "cmd"):
                continue
            if self.match_command(package.cmd, cmd_name, delimiters):
                if package.cmd_type not in commands:
                    commands[package.cmd_type] = []
                if package.enabled:
                    commands[package.cmd_type].append(package)
            elif package.aliases:
                for alias in package.aliases:
                    if self.match_command(alias, cmd_name, delimiters):
                        if package.cmd_type not in commands:
                            commands[package.cmd_type] = []
                        if package.enabled:
                            commands[package.cmd_type].append(package)
                        break
        
        if not commands:
            await send_msg.send_error(f"\"{cmd_name}\" is Not A Valid Command")
        else:
            text_buffers: list[list[str]] = []
            for cmd_type in commands:
                text_buffer: list[str] = []
                for package in commands[cmd_type]:
                    text_buffer.append(f"**{package.component}**")
                    if package.description:
                        text_buffer.append("")
                        text_buffer.append(package.description.replace("\n", "\n> "))
                        text_buffer.append("")
                    
                    text_buffer.append("**trigger:**")
                    if isinstance(package.cmd, str):
                        text_buffer.append(f"  - **cmd:** {package.cmd}")
                    elif isinstance(package.cmd, tuple):
                        text_buffer.append("  - **cmd:**")
                        for cmd in self.all_joined_commands(package.cmd, delimiters):
                            text_buffer.append(f"    - {cmd}")
                    else:
                        raise TypeError(f"{package.cmd} is not a valid command")
                    
                    if package.aliases:
                        text_buffer.append("  - **aliases:**")
                        for alias in package.aliases:
                            if isinstance(alias, str):
                                text_buffer.append(f"    - {alias}")
                            elif isinstance(alias, tuple):
                                for sub_alias in self.all_joined_commands(alias, delimiters):
                                    text_buffer.append(f"    - {sub_alias}")
                            else:
                                raise TypeError(f"{alias} is not a valid alias")
                text = "\n".join(text_buffer)
                if text:
                    text_buffers.append(text_buffer)
            
            text = "\n\n---\n\n".join("\n".join(buffer) for buffer in text_buffers)
            if not text:
                await send_msg.send_error("Text Buffer is Empty")
            await send_msg.send_render_prompt(text)
