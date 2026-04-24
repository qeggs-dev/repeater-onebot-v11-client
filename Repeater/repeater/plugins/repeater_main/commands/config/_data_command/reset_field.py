from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class ResetField(BaseConfig):
    cmd = "resetConfigField"
    aliases = {
        "rcf",
        "RCF",
        "reset_config_field",
        "Reset_Config_Field",
        "ResetConfigField",
        "RESET_CONFIG_FIELD",
    }

    async def parse_value_free(self, persona_info: PersonaInfo, send_msg: SendMsg):
        field = persona_info.message_striped_str
        return field, None
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Reseted Field {field}")