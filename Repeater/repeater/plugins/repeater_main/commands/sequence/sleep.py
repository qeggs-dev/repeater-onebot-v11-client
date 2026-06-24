from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import VersionAPIClient
from ..._adaptation_info import __adaptation__


@CommandCaller.register
class Sleep(CommandPackage):
    cmd = "sleep"
    aliases = {
        "s",
        "S",
        "Sleep",
        "SLEEP",
    }
    cmd_type = CmdTypes.SEQUENCE

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        try:
            sleep_time = int(persona_info.message_striped_str)
        except ValueError:
            await send_msg.send_error("Please enter a valid number")
            return
        
        