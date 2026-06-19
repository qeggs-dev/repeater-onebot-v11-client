from ...assist import PersonaInfo, SendMsg, Response
from ...command_register import CommandCaller
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
    
    async def send_result(self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response[None]):
        if response:
            await send_msg.send_render(response.text)
        else:
            await send_msg.send_response_check_code(response)