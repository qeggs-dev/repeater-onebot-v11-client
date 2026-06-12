from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import CommandCaller
from ...clients import TemplateRenderClient
from ._template_render import TemplateRender

@CommandCaller.register
class TemplateRenderImage(TemplateRender):
    cmd = "templateRenderImage"
    aliases = {
        "tri",
        "TRI",
        "template_render_image",
        "Template_Render_Image",
        "TemplateRenderImage",
        "TEMPLATE_RENDER_IMAGE",

        # Reserved for compatibility.
        "vei",
        "VEI",
        "var_expand_image",
        "Var_Expand_Image",
        "VarExpandImage",
        "VAR_EXPAND_IMAGE",
    }

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str
        variable_expansion_client = TemplateRenderClient(persona_info)
        response = await variable_expansion_client.render(text=msg)
        if response.code == 200:
            await send_msg.send_render(response.text)
        else:
            await send_msg.send_response_check_code(response)