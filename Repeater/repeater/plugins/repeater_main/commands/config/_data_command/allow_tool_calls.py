from ....assist import PersonaInfo, SendMsg, Response, str_to_bool
from ....command_register import CommandCaller
from ..._bases import BaseConfig

@CommandCaller.register
class AllowToolCalls(BaseConfig):
    cmd = "allowToolCalls"
    aliases= {
        "atc",
        "ATC",
        "allow_tool_calls",
        "Allow_Tool_Calls",
        "AllowToolCalls",
        "ALLOW_TOOL_CALLS",
    }
    field = "allow_tool_calls"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> bool:
        try:
            thinking = str_to_bool(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Not a valid boolean value")
        
        return thinking
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        await send_msg.send_response_check_code(response, f"Tool Calls is {value}")