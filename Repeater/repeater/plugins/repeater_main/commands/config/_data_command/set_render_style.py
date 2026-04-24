from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetRenderStyle(BaseConfig):
    cmd = "setRenderStyle"
    aliases = {
        "srs",
        "SRS",
        "set_render_style",
        "Set_Render_Style",
        "SetRenderStyle",
        "SET_RENDER_STYLE",
    }
    field = "render_style"
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Set Render_Style to {value}")