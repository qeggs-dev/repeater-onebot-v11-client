from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller
from .._clients import TemplateRenderClient
from ._template_render import TemplateRender

@CommandCaller.register
class TemplateRenderText(TemplateRender):
    cmd = "templateRenderText"
    aliases = {
        "trt",
        "TRT",
        "template_render_text",
        "Template_Render_Text",
        "TemplateRenderText",
        "TEMPLATE_RENDER_TEXT",

        # Reserved for compatibility.
        "vet",
        "VET",
        "var_expand_text",
        "Var_Expand_Text",
        "VarExpandText",
        "VAR_EXPAND_TEXT",
    }

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str
        variable_expansion_client = TemplateRenderClient(persona_info)
        response = await variable_expansion_client.render(text=msg)
        if response.code == 200:
            await send_msg.send_text(response.text)
        else:
            await send_msg.send_response_check_code(response)