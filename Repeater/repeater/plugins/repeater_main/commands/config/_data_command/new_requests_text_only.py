from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetNewRequestsTextOnly(BaseConfig):
    cmd = "setNewRequestsTextOnly"
    aliases = {
        "nrto",
        "NRTO",
        "set_new_requests_text_only",
        "Set_New_Requests_Text_Only",
        "SetNewRequestsTextOnly",
        "SET_NEW_REQUESTS_TEXT_ONLY",
    }
    field = "new_requests_text_only"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> bool:
        try:
            value = str_to_bool(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Not a valid boolean value")
        return value

    async def finish_message(
        self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response, value: bool
    ) -> None:
        await send_msg.send_response_check_code(response, f"New Requests Text Only set to {value}")