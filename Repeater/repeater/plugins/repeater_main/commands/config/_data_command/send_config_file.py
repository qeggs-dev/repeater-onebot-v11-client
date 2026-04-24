from ....assist import PersonaInfo, SendMsg, Response, FileSender
from ....command_register import CommandCaller
from ..._bases import BaseConfig, OperationType


@CommandCaller.register
class SendConfigFile(BaseConfig):
    cmd = "sendConfigFile"
    aliases = {
        "scfgf",
        "SCFGF",
        "send_config_file",
        "Send_Config_File",
        "SendConfigFile",
        "SCFGF"
    }
    operation = OperationType.GET_FILE_URL

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> None:
        return None
    
    async def finish_message(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            response: Response,
            field: str,
            value: bool
        ):
        if value:
            file_sender = FileSender(
                persona_info=persona_info,
                send_msg=send_msg
            )
            await file_sender.send_file(value, f"{persona_info.namespace_str}_User_Config.json")
        else:
            await send_msg.send_error("Failed to get config file URL")