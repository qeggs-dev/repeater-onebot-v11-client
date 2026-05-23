from ...assist import PersonaInfo, SendMsg, Response
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from .._clients import TemplateRenderClient

@CommandCaller.register
class TemplateRender(CommandPackage):
    cmd = "templateRender"
    aliases = {
        "tr",
        "TR",
        "template_render",
        "Template_Render",
        "TemplateRender",
        "TEMPLATE_RENDER",

        # Reserved for compatibility.
        "varExpand",
        "ve",
        "VE",
        "var_expand",
        "Var_Expand",
        "VarExpand",
        "VAR_EXPAND",
    }
    cmd_type = CmdTypes.TEMPLATE

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str
        variable_expansion_client = TemplateRenderClient(persona_info)
        response = await variable_expansion_client.render(text = msg)
        await self.send_result(persona_info, send_msg, response)
    
    async def send_result(self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response[None]):
        if response.code == 200:
            await send_msg.send_check_length(response.text)
        else:
            await send_msg.send_response_check_code(response)