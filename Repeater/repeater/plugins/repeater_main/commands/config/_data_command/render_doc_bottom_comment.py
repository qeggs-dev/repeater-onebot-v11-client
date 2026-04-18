from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ConfigClient
from ....assist import PersonaInfo, SendMsg

render_doc_bottom_comment = on_command("renderDocBottomComment", aliases={"rdbc", "render_doc_bottom_comment", "Render_Doc_Bottom_Comment", "RenderDocBottomComment"}, rule=to_me(), block=True)

@render_doc_bottom_comment.handle()
async def handle_render_doc_bottom_comment(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Render_Doc_Bottom_Comment", render_doc_bottom_comment, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    msg = persona_info.message_striped_str

    config_client = ConfigClient(persona_info)
    response = await config_client.set_config("render_document_bottom_comment", msg)
    await send_msg.send_response_check_code(response, f"Set Render Document Bottom Comments to {msg}")