from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from .._clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger

keep_reasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keep_reasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)
    send_msg = SendMsg(
        "Chat.Keep_Reasoning",
        keep_reasoning,
        persona_info
    )

    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()

    logger.info(
        "Received a message from {namespace}",
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    chat_client = ChatClient(persona_info)

    response = await chat_client.send_message(
        thinking=True,
    )
    
    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        keep_reasoning,
        response
    )
    await send_msg.send()
