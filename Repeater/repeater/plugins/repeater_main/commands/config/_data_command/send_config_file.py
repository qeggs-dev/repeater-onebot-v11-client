from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, FileSender, SendMsg

send_config_file = on_command("sendConfigFile", aliases={"scfgf", "send_config_file", "Send_Config_File", "SendConfigFile"}, rule=to_me(), block=True)

@send_config_file.handle()
async def handle_send_config_file(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot=bot, event=event)
    send_msg = SendMsg("Config.Send_Config_File", send_config_file, persona_info)

    user_file_client = ConfigClient(persona_info)
    file_url = user_file_client.get_config_url()
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        file_sender = FileSender(
            persona_info = persona_info,
            send_msg = send_msg
        )

        await file_sender.send_file(file_url, f"{persona_info.namespace_str}_User_Config.json")
