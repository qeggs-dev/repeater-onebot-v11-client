from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from ...assist import PersonaInfo, SendMsg

@CommandCaller.register
class CmdTypesList(CommandPackage):
    cmd = "cmdTypesList"
    aliases = {
        "ctl",
        "CTL",
        "cmd_types_list",
        "Cmd_Types_List",
        "CmdTypesList",
        "CMD_TYPES_LIST"
    }
    cmd_type = CmdTypes.SEE_CMD
    documents = f"""
        List all command types.

        Usage:
        ```
        /{cmd}
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        commands_count: dict[CmdTypes, int] = {}
        total_count: int = 0

        for package in CommandCaller.commands.values():
            if package.enabled:
                if package.cmd_type not in commands_count:
                    commands_count[package.cmd_type] = 0
                commands_count[package.cmd_type] += 1
                total_count += 1
        
        text_buffer: list[str] = []
        text_buffer.append(f"Total: {total_count}")
        for cmd_type, count in commands_count.items():
            text_buffer.append(f"{cmd_type.value} ({count}: {count / total_count:.2%})")
        
        await send_msg.send_check_length_prompt(
            "\n".join(text_buffer)
        )
