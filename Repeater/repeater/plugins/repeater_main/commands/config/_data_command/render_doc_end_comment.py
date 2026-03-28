from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigCore
from ....assist import PersonaInfo, SendMsg

render_doc_end_comment = on_command("renderDocEndComment", aliases={"rdec", "render_doc_end_comment", "Render_Doc_End_Comment", "RenderDocEndComment"}, rule=to_me(), block=True)

@render_doc_end_comment.handle()
async def handle_render_doc_end_comment(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Render_Doc_End_Comment", persona_info, render_doc_end_comment, None)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_striped_str

    config_core = ConfigCore(persona_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("render_document_end_comments", msg)
        await send_msg.send_response_check_code(response, f"Set Max_Tokens to {msg}")