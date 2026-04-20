from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetMultipleModel(BaseConfig):
    cmd = "setMultipleModel"
    aliases = {
        "smm",
        "SMM",
        "set_multiple_model",
        "Set_Multiple_Model",
        "SetMultipleModel",
        "SET_MULTIPLE_MODEL",
    }
    field = "model_uid"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> list[str]:
        msg = persona_info.message_striped_str
        value = parse_delimited_string(msg)
        if not value:
            await send_msg.send_error("Please enter at least one model_uid")
        return value

    async def finish_message(
        self, persona_info: PersonaInfo, send_msg: SendMsg, response: Response, value: list[str]
    ) -> None:
        await send_msg.send_response_check_code(response, f"Set Multiple Model to {', '.join(value)}")