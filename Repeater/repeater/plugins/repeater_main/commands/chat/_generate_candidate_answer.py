from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, SendMsg

generate_candidate_answer: type[Matcher] = on_command("generateCandidateAnswer", aliases={"gca", "generate_candidate_answer", "Generate_Candidate_Answer", "GenerateCandidateAnswer"}, rule=to_me(), block=True)

@generate_candidate_answer.handle()
async def handle_generate_candidate_answer(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg(
        "Chat.Generate_Candidate_Answer",
        generate_candidate_answer,
        persona_info
    )

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    message_text = persona_info.message_str.strip()

    logger.info(
        "Received a message {message} from {namespace}",
        message = message_text,
        namespace = persona_info.namespace_str,
        module = send_msg.component
    )

    try:
        number = int(message_text)
    except ValueError:
        try:
            number = float(message_text)
        except ValueError:
            send_msg.send_error("Please enter a number")

    meta_prompt = [
        "I do not know how to reply to you, please provide some simple candidates",
        "Use the following format:",
        "",
        "1. Answer 1",
        "2. Answer 2",
        "3. Answer 3",
        "...",
        "",
        "And so on",
        f"Finally, {number} answers are generated."
    ]

    meta_prompt_str = "\n".join(meta_prompt)
    
    reply_msgs = await persona_info.get_reply_chain()
    if reply_msgs:
        reply_msgs_text = persona_info.generates_text_from_messages_list(reply_msgs)
        reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")
        if meta_prompt_str:
            meta_prompt_str = f"{reply_msgs_text}\n\n---\n\n{meta_prompt_str}"
        else:
            meta_prompt_str = reply_msgs_text

    core = ChatCore(persona_info)

    images: list[str] = await persona_info.get_images_url()

    response = await core.send_message(
        message = meta_prompt_str,
        save_context = False,
        image_url = images
    )

    send_msg = ChatSendMsg(
        send_msg.component,
        persona_info,
        generate_candidate_answer,
        response
    )
    await send_msg.send()