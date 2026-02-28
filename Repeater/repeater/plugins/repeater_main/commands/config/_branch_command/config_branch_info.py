from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

config_branch_info = on_command("configBranchInfo", aliases={"cfgbi", "config_branch_info", "Config_Branch_Info", "ConfigBranchInfo"}, rule=to_me(), block=True)

@config_branch_info.handle()
async def handle_config_branch_info(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Config_Branch_Info", config_branch_info, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.branch_info()
        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")

            text_buffer: list[str] = []
            text_buffer.append(f"Branch Type: Config")
            text_buffer.append(f"Branch ID: {data.branch_id}")
            if data.file_exists:
                text_buffer.append(f"Branch Size: {data.size}")
                text_buffer.append(f"Branch Readable Size: {data.readable_size}")
                text_buffer.append(f"Branch Last Modified Time: {data.modified_datetime().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                text_buffer.append("Branch File Not Exists")

            await send_msg.send_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response, "Get Config branch info failed")