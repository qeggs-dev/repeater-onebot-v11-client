from nonebot.adapters.onebot.v11 import Bot

async def send_private_file(
    bot: Bot,
    user_id: str,
    url: str,
    file_name: str,
):
    data = {
        "user_id": user_id,
        "file": url,
        "name": file_name
    }
    await bot.upload_private_file(**data)