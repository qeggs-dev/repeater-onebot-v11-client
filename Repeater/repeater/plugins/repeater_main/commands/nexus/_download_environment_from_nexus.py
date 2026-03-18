from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import NexusCore
from ...assist import PersonaInfo, SendMsg

environment_download_from_nexus = on_command("envDownloadFromNexus", aliases={"edfn", "env_download_from_nexus", "Env_Download_From_Nexus", "EnvDownloadFromNexus"}, rule=to_me(), block=True)

@environment_download_from_nexus.handle()
async def handle_environment_download_from_nexus(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Nexus.Download_Environment_From_Nexus", environment_download_from_nexus, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    nexus_core = NexusCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        try:
            response = await nexus_core.download_environment_from_nexus(persona_info.message_striped_str)
        except ValueError as e:
            await send_msg.send_error(
                f"Invalid UUID: {persona_info.message_striped_str}"
            )

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
            else:
                await send_msg.send_prompt(
                    f"Download successful."
                )
        else:
            await send_msg.send_response_check_code(response, "Unable to download environment from Nexus.")