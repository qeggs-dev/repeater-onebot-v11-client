from ..assist import PersonaInfo, SendMsg
from ..cmd_info import CmdTypes
from ..command_register import(
    CommandCaller,
    CommandPackage
)


@CommandCaller.register
class TextRender(CommandPackage):
    cmd = "markdownRender"
    aliases = {
        "mr",
        "MR",
        "markdown_render",
        "Markdown_Render",
        "MarkdownRender",
        "MARKDOWN_RENDER",
    }
    cmd_type = CmdTypes.RENDER

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        await send_msg.send_render(persona_info.message_striped_str)