from ..assist import PersonaInfo, SendMsg
from ..command_register import CommandCaller, CommandPackage


@CommandCaller.register
class TextRender(CommandPackage):
    cmd = "textRender"
    aliases = {
        "tr",
        "TR",
        "text_render",
        "Text_Render",
        "TextRender",
        "TEXT_RENDER",
    }

    @property
    def component(self) -> str:
        return f"Render.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        await send_msg.send_render(persona_info.message_striped_str)