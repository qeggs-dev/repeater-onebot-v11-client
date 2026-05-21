from nonebot import on_message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg, MessageSource
from ...command_register import CommandCaller, CommandPackage, ListenType

@CommandCaller.register
class SmartAt(CommandPackage):
    listen_type: ListenType = ListenType.Message
    component = "Chat.Smart_at"
    priority = 100
    documents = """
        Determines whether the input is null,
        to perform a build task,
        or output the specified text

        Usage:
        ```
        @Bot message
        ```

        Or:
        ```
        @Bot
        ```
    """

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message {message} from {namespace}",
            message = persona_info.message_striped_str,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )
        
        if not persona_info:
            if persona_info.source == MessageSource.GROUP:
                await send_msg.send_hello()
            else:
                return
        
        core = ChatClient(persona_info)

        message = persona_info.message
        if not message:
            logger.warning("Message is empty")
            return
        
        message_text = persona_info.message_striped_str

        forward_msgs = await persona_info.get_forward_msgs()
        if forward_msgs:
            forward_msgs_text = persona_info.generates_text_from_messages_list(forward_msgs)
            if message_text:
                message_text = f"Forwarded messages:\n{forward_msgs_text}\n\n---\n\n{message_text}"
            else:
                message_text = forward_msgs_text
        else:
            message_text = message_text
        
        reply_msgs = await persona_info.get_reply_chain()
        if reply_msgs:
            reply_msgs_text = persona_info.generates_text_from_messages_list(reply_msgs)
            reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")
            if message_text:
                message_text = f"Reply messages:\n{reply_msgs_text}\n\n---\n\n{message_text}"
            else:
                message_text = reply_msgs_text

        images: list[str] = await persona_info.get_images_url()
        audios: list[str] = await persona_info.get_audio_url()
        videos: list[str] = persona_info.get_video_url()

        if not images:
            if not message_text:
                message = str(message)

        response = await core.send_message(
            message = message_text,
            image_url = images,
            audio_url = audios,
            video_url = videos,
        )
        
        chat_send_msg = ChatSendMsg(
            send_msg.component,
            persona_info,
            send_msg.matcher,
            response
        )
        await chat_send_msg.send()