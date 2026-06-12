from ..assist import PersonaInfo, SendMsg
from ..cmd_info import CmdTypes
from ..command_register import(
    CommandCaller,
    CommandPackage
)
from ..clients import VersionAPIClient
from .._adaptation_info import __adaptation__


@CommandCaller.register
class AdaptationInfo(CommandPackage):
    cmd = "adaptationInfo"
    aliases = {
        "adai",
        "ADAI",
        "adaptation_info",
        "Adaptation_Info",
        "AdaptationInfo",
        "ADAPTATION_INFO",
    }
    cmd_type = CmdTypes.VERSION

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        version_client = VersionAPIClient()
        server_version = await version_client.get_version()
        version_data = server_version.get_data()
        if version_data is None:
            await send_msg.send_error("Server Version Data is Invalid")
            return
        await send_msg.send_prompt(
            (
                f"Client Adaptation Version: {__adaptation__}\n"
                f"Server Core Version: {version_data.core}"
            )
        )