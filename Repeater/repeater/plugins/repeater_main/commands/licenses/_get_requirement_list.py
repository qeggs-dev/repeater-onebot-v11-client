from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from .._clients import LicenseClient


@CommandCaller.register
class GetRequirementList(CommandPackage):
    cmd = "getRequirementList"
    aliases = {
        "grls",
        "GRLS",
        "get_requirement_list",
        "Get_Requirement_List",
        "GetRequirementList",
        "GET_REQUIREMENT_LIST",
    }
    cmd_type = CmdType.LICENSES

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        license_client = LicenseClient()
        server_requirements = await license_client.get_requirement_list()
        version_data = server_requirements.get_data()
        if not version_data:
            await send_msg.send_error("Server requirements data is invalid.")
        else:
            text_buffer: list[str] = []
            for index, requirement in enumerate(version_data, start=1):
                text_buffer.append(f"{index}. {requirement}")
            await send_msg.send_check_length("\n".join(text_buffer))