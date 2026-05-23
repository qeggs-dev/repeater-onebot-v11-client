from ...assist import PersonaInfo, SendMsg, FileSender, FileUrl
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
import time


@CommandCaller.register
class AudioToFile(CommandPackage):
    cmd = "audioToFile"
    aliases = {
        "a2f",
        "A2F",
        "audio_to_file",
        "Audio_To_File",
        "AudioToFile",
        "AUDIO_TO_FILE",
    }
    cmd_type = CmdTypes.OTHER

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        for message_segment in persona_info.message:
            if message_segment.type == "record":
                file_sender = FileSender(
                    persona_info=persona_info,
                    send_msg=send_msg
                )
                fileurl = FileUrl(message_segment.data["url"])
                await file_sender.send_file(
                    url=str(fileurl),
                    file_name=f"{persona_info.nickname}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}{fileurl.path.suffix}"
                )