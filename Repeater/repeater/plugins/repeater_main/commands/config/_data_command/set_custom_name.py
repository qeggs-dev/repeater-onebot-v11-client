from ....assist import PersonaInfo, SendMsg, Response
from ....command_register import CommandCaller
from ..._bases import BaseConfig


@CommandCaller.register
class SetCustomName(BaseConfig):
    cmd = "setCustomName"
    aliases = {
        "scn",
        "SCN",
        "set_custom_name",
        "Set_Custom_Name",
        "SetCustomName",
        "SET_CUSTOM_NAME",
    }
    field = "user_name"
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: str
        ):
        await send_msg.send_response_check_code(response, f"Custom Name set to {value}")