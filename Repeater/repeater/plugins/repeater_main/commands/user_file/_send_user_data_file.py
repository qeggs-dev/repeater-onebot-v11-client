from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import UserFileClient
from ...assist import PersonaInfo, FileSender, SendMsg

send_user_data_file = on_command("sendUserDataFile", aliases={"sudf", "send_user_data_file", "Send_User_Data_File", "SendUserDataFile"}, rule=to_me(), block=True)

@send_user_data_file.handle()
async def handle_send_user_data_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("UserFile.Send_User_Data_File", send_user_data_file, persona_info)

    user_file_client = UserFileClient(persona_info)
    file_url = await user_file_client.get_user_data_file_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(
            persona_info = persona_info,
            send_msg = send_msg,
        )

        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_UserDataFile.zip")
