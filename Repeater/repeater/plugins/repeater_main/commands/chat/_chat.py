from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg

chat: type[Matcher] = on_command("chat", aliases={"c", "Chat"}, rule=to_me(), block=True)

@chat.handle()
async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Chat",
        chat,
        persona_info
    )

    if send_msg.is_debug_mode:
        send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_striped_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    message_text = persona_info.message_striped_str
    
    reply_msgs = await persona_info.get_reply_chain()
    if reply_msgs:
        reply_msgs_text = persona_info.generates_text_from_messages_list(reply_msgs)
        reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")
        if message_text:
            message_text = f"{reply_msgs_text}\n\n---\n\n{message_text}"
        else:
            message_text = reply_msgs_text

    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = message_text,
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        chat,
        response
    )
    await send_msg.send_text_mode()