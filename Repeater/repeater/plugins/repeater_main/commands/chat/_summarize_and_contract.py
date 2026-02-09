from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...core_net_configs import storage_configs

summarize_and_contract: type[Matcher] = on_command("summarizeAndContract", aliases={"sac", "summarize_and_contract", "Summarize_And_Contract", "SummarizeAndContract"}, rule=to_me(), block=True)

@summarize_and_contract.handle()
async def handle_summarize_and_contract(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Summarize_And_Contract",
        summarize_and_contract,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    message_text = persona_info.message_str.strip()
    if not message_text:
        message_text = storage_configs.summarize_and_contract_default_message
    
    reply_msgs = await persona_info.get_reply_msgs()
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
        image_url = images,
        save_new_only = True
    )

    chat_send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        summarize_and_contract,
        response
    )

    await chat_send_msg.send()