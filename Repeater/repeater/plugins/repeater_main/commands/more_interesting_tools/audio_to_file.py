import time

from pathlib import Path
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)

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
        for message_segment in persona_info.message:
            if message_segment.type == "record":
                fileurl = message_segment.data["url"]
                path = Path(fileurl)
                await send_msg.send_file(
                    url = str(fileurl),
                    file_name = f"{persona_info.nickname}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}{path.suffix}"
                )