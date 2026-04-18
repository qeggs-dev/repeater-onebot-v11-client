from ._persona_info import PersonaInfo, MessageSource
from ._send_msg import SendMsg
from nonebot.exception import ActionFailed
from nonebot import logger

class FileSender:
    def __init__(self, persona_info: PersonaInfo, send_msg: SendMsg):
        self.persona_info = persona_info
        self.send_msg = send_msg

    async def send_file(self, url: str, file_name: str):
        try:
            if self.persona_info.source == MessageSource.GROUP:
                data = {
                    "group_id": self.persona_info._group_id,
                    "file": url,
                    "name": file_name
                }
                await self.persona_info.bot.upload_group_file(**data)
            elif self.persona_info.source == MessageSource.PRIVATE:
                data = {
                    "user_id": self.persona_info.user_id,
                    "file": url,
                    "name": file_name
                }
                await self.persona_info.bot.upload_private_file(**data)
        except ActionFailed as e:
            logger.error(f"Failed to upload file: {e}")
            self.send_msg.send_error("Failed to upload file.")