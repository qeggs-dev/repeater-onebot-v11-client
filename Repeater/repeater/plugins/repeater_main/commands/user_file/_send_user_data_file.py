from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import UserFileClient


@CommandCaller.register
class SendUserDataFile(CommandPackage):
    cmd = "sendUserDataFile"
    aliases = {
        "sudf",
        "SUDF",
        "send_user_data_file",
        "Send_User_Data_File",
        "SendUserDataFile",
        "SEND_USER_DATA_FILE",
    }
    cmd_type = CmdTypes.USERFILE

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        user_file_client = UserFileClient(persona_info)
        file_url = await user_file_client.get_user_data_file_url()
        await send_msg.send_file(file_url, f"{persona_info.namespace_str}_UserDataFile.zip")