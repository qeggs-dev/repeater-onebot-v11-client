from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import UserFileClient
from ...assist import PersonaInfo, FileSender, SendMsg

package_user_space = on_command("packageUserSpace", aliases={"pus", "package_user_space", "Package_User_Space", "PackageUserSpace"}, rule=to_me(), block=True)

@package_user_space.handle()
async def handle_package_user_space(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("UserFile.Package_User_Space", package_user_space, persona_info)

    user_file_client = UserFileClient(persona_info)
    file_url = await user_file_client.package_user_space_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(
            persona_info = persona_info,
            send_msg = send_msg,
        )

        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_PackageSpace.zip")
