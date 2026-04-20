from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller, CommandPackage
from .._clients import VariableExpansionClient


@CommandCaller.register
class VarExpandImage(CommandPackage):
    cmd = "varExpandImage"
    aliases = {
        "vei",
        "VEI",
        "var_expand_image",
        "Var_Expand_Image",
        "VarExpandImage",
        "VAR_EXPAND_IMAGE",
    }

    @property
    def component(self) -> str:
        return f"VarExpand.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str
        variable_expansion_client = VariableExpansionClient(persona_info)
        response = await variable_expansion_client.expand_variable(text=msg)
        if response.code == 200:
            await send_msg.send_render(response.text)
        else:
            await send_msg.send_response_check_code(response)