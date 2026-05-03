import json
from ....assist import PersonaInfo, SendMsg, Response, parse_delimited_string
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType

@CommandCaller.register
class RemovePresetDirectives(BaseConfig):
    cmd = "removePresetDirectives"
    aliases= {
        "rpd",
        "RPD",
        "remove_preset_directives",
        "Remove_Preset_Directives",
        "RemovePresetDirectives",
        "REMOVE_PRESET_DIRECTIVES",
    }
    field = "prompt_directives"
    operation = OperationType.GET_AND_SET

    async def parse_value(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        raw_value: dict[str, list[str]] | None = None
    ):
        removed_diretives = parse_delimited_string(persona_info.message_striped_str)
        for tool in removed_diretives:
             if tool in raw_value:
                del raw_value[tool]
                 
             
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: list[str] | None
        ):
            await send_msg.send_response_check_code(response, f"Removed Preset Directives to {json.dumps(value, ensure_ascii = False)}")