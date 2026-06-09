from nonebot.adapters.onebot.v11 import Bot

async def send_group_file(
    bot: Bot,
    group_id: int,
    url: str,
    file_name: str,
):
    data = {
        "group_id": group_id,
        "file": url,
        "name": file_name
    }
    await bot.upload_group_file(**data)