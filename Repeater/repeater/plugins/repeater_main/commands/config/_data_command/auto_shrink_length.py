from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetAutoShrinkLength(BaseConfig):
    cmd = "setAutoShrinkLength"
    aliases = {
        "sasl",
        "SASL",
        "set_auto_shrink_length",
        "Set_Auto_Shrink_Length",
        "SetAutoShrinkLength",
        "SET_AUTO_SHRINK_LENGTH"
    }
    field = "context_shrink_limit"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> int:
        try:
            value = int(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Message must be a number")
        return value

    async def finish_message(
        self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response, value: int
    ) -> None:
        await send_msg.send_response_check_code(response, f"Auto shrink length set to {value}")