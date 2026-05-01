from ...assist import PersonaInfo, SendMsg, FileSender
from ...command_register import CommandCaller, CommandPackage
from .._clients import UserFileClient


@CommandCaller.register
class PackageUserSpace(CommandPackage):
    cmd = "packageUserSpace"
    aliases = {
        "pus",
        "PUS",
        "package_user_space",
        "Package_User_Space",
        "PackageUserSpace",
        "PACKAGE_USER_SPACE",
    }

    @property
    def component(self) -> str:
        return f"UserFile.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        user_file_client = UserFileClient(persona_info)
        file_url = await user_file_client.package_user_space_url()
        file_sender = FileSender(
            persona_info=persona_info,
            send_msg=send_msg,
        )
        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_PackageSpace.zip")