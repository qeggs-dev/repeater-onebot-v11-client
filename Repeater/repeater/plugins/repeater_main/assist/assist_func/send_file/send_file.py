from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from ...namespace import MessageSource

async def send_file(
    bot: Bot,
    group_id: int,
    user_id: int,
    url: str,
    file_name: str,
    source: MessageSource,
):
    match source:
        case MessageSource.GROUP:
            data = {
                "group_id": group_id,
                "file": url,
                "name": file_name
            }
            await bot.upload_group_file(**data)
        case MessageSource.PRIVATE:
            data = {
                "user_id": user_id,
                "file": url,
                "name": file_name
            }
            await bot.upload_private_file(**data)