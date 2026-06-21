from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

async def get_message_event(bot: Bot, message_id: int) -> MessageEvent:
    response = await bot.get_msg(
        message_id = message_id
    )
    post_type = response["post_type"]
    # 兼容 MessageEvent
    if post_type != "message":
        response["post_type"] = "message"
        logger.warning(
            "Changing the post_type from \"{post_type}\" to \"message\" may cause some unusual behavior.",
            post_type = post_type
        )
    return MessageEvent(**response)