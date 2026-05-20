from typing import NoReturn
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg
from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandPackage, CmdType

class BaseChat(CommandPackage):
    type = CmdType.CHAT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message {message} from {namespace}",
            message = persona_info.message_striped_str,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )

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
        
        client = self.get_client(persona_info)

        response = await self.send_message(
            client = client,
            images = images,
            audios = audios,
            videos = videos,
            message = message_text,
            persona_info = persona_info,
            send_msg = send_msg
        )
        
        chat_send_msg = ChatSendMsg(
            component = send_msg.component,
            persona_info = persona_info,
            matcher = send_msg.matcher,
            response = response
        )
        await self.send_chat_send_msg(chat_send_msg)
    
    def get_client(self, persona_info: PersonaInfo) -> ChatClient:
        client = ChatClient(persona_info)
        return client
    
    async def send_message(
        self,
        client: ChatClient,
        images: list[str],
        audios: list[str],
        videos: list[str],
        message: str,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> str:
        response = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
        )
        return response
    
    async def send_chat_send_msg(self, chat_send_msg: ChatSendMsg) -> NoReturn:
        await chat_send_msg.send()