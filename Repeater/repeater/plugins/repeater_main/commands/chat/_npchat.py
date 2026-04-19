from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from .._clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...logger import logger

npchat = on_command("npChat", aliases={"np", "no_prompt_chat", "No_Prompt_Chat", "NoPromptChat"}, rule=to_me(), block=True)

@npchat.handle()
async def handle_npchat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.No_Prompt_Chat",
        npchat,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_striped_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component,
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

    chat_client = ChatClient(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await chat_client.send_message(
        message_text,
        image_url = images,
        load_prompt = False,
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        npchat,
        response
    )
    await send_msg.send()