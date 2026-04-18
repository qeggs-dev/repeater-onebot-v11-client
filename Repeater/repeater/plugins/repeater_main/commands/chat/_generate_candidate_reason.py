import re

from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg, ContentRole
from ...assist import PersonaInfo, SendMsg

generate_candidate_reason: type[Matcher] = on_command("generateCandidateReason", aliases={"gcr", "generate_candidate_reason", "Generate_Candidate_Reason", "GenerateCandidateReason"}, rule=to_me(), block=True)

metadata_pattern = re.compile(r"> Message\s*?Metadata:.*?---(?:\r?\n)+", re.DOTALL | re.IGNORECASE)

@generate_candidate_reason.handle()
async def handle_generate_candidate_reason(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Generate_Candidate_Reason",
        generate_candidate_reason,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    message_text = persona_info.message_striped_str

    logger.info(
        "Received a message {message} from {namespace}",
        message = message_text,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )
    
    reply_msgs = await persona_info.get_reply_chain()
    if reply_msgs:
        reply_msgs_text = persona_info.generates_text_from_messages_list(reply_msgs)
        reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")

    core = ChatClient(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = None,
        add_metadata = False,
        save_context = False,
        temporary_prompt = (
            "{%- if user_profile -%}\n"
            "{{user_profile}}\n"
            "{%- endif %}"
        ),
        history_msg_role_map = {
            ContentRole.USER: ContentRole.ASSISTANT,
            ContentRole.ASSISTANT: ContentRole.USER,
            ContentRole.SYSTEM: None,
            ContentRole.TOOLS: None
        },
        image_url = images,
        thinking = True,
    )

    def filters(message: str) -> str:
        return metadata_pattern.sub("", message)

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        generate_candidate_reason,
        response,
        content_handler = filters
    )
    await send_msg.send()