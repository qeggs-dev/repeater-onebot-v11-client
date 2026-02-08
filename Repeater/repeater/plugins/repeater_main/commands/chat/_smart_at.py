from nonebot import on_message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg, MessageSource

smart_at: type[Matcher] = on_message(rule=to_me(), priority=100, block=True)

@smart_at.handle()
async def handle_smart_at(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)
    send_msg = SendMsg(
        "Chat.Smart_at",
        smart_at,
        persona_info
    )

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )
    
    if not persona_info:
        if persona_info.source == MessageSource.GROUP:
            await send_msg.send_hello()
        else:
            return
    
    core = ChatCore(persona_info)

    message = persona_info.message
    if not message:
        logger.warning("Message is empty")
        return
    
    message_str = persona_info.message_str

    forward_msgs = await persona_info.get_forward_msgs()
    if forward_msgs:
        forward_msgs_text = persona_info.generates_text_from_messages_list(forward_msgs)
        if message_str:
            message_text = f"{forward_msgs_text}\n\n---\n\n{message_str}"
        else:
            message_text = forward_msgs_text
    else:
        message_text = message_str

    images: list[str] = await persona_info.get_images_url()

    if not images:
        if not message_text:
            message = str(message)

    response = await core.send_message(
        message = message_text,
        image_url = images
    )
    
    chat_send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        smart_at,
        response
    )
    await chat_send_msg.send()