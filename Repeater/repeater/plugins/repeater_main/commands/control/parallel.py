import re

from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import VersionAPIClient
from ..._adaptation_info import __adaptation__


@CommandCaller.register
class Parallel(CommandPackage):
    cmd = "parallel"
    aliases = {
        "p",
        "P",
        "Parallel",
        "PARALLEL",
    }
    cmd_type = CmdTypes.CONTROL

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        lines = persona_info.message_striped_str.splitlines()
        