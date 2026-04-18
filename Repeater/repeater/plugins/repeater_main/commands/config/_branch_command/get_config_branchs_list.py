from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg

get_config_branchs_list = on_command("getConfigBranchsList", aliases={"gcfgbl", "get_config_branchs_list", "Get_Config_Branchs_List", "GetConfigBranchsList"}, rule=to_me(), block=True)

@get_config_branchs_list.handle()
async def handle_config_branchs_list(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Get_Config_Branchs_List", get_config_branchs_list, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    config_client = ConfigClient(persona_info)
    response = await config_client.get_branch_list()
    if response.code == 200:
        data = response.json()
        if not isinstance(data, list):
            await send_msg.send_error("Unable to process data.")

        text_buffer: list[str] = []
        text_buffer.append(f"Branch Type: Config")
        text_buffer.append(f"User Name: {persona_info.display_name}")
        if data:
            text_buffer.append("Branchs:")
            for branch_id in data:
                text_buffer.append(f"  - {branch_id}")
        else:
            text_buffer.append("No branchs found.")

        await send_msg.send_check_length_prompt("\n".join(text_buffer))
    else:
        await send_msg.send_response_check_code(response, "Get Config branch list failed")