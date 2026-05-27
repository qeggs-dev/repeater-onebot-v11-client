from typing import NoReturn, ClassVar
from itertools import chain

from ...logger import logger
from .._clients import ChatClient, ChatSendMsg, ChatResponse
from ...assist import PersonaInfo, SendMsg, Response
from ...command_register import CommandPackage, CmdTypes
from pydantic import BaseModel

class Message(BaseModel):
    text: str | None = None
    images: list[str] | None = None
    audios: list[str] | None = None
    videos: list[str] | None = None

class BaseChat(CommandPackage):
    cmd_type = CmdTypes.CHAT
    empty_exit: ClassVar[bool] = True
    no_input: ClassVar[bool] = False

    async def empty_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ):
        logger.warning("Message is empty")
        if self.empty_exit:
            send_msg.break_handler()
    
    async def parse_forward_msgs(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> str:
        forward_msgs = await persona_info.get_forward_msgs()
        if forward_msgs:
            forward_msgs_text = persona_info.generates_text_from_messages_list(forward_msgs)
            message_text = f"Forwarded messages:\n{forward_msgs_text}\n\n---\n\n{message_text}"
        else:
            message_text = ""
        
        return message_text

    async def parse_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> Message:
        if self.no_input:
            return Message()
        else:
            message = persona_info.message
            if not persona_info:
                await self.empty_message(persona_info, send_msg)
            
            message_text = persona_info.message_striped_str

            message_text += await self.parse_forward_msgs(persona_info, send_msg)

            images: list[str] = await persona_info.get_images_url()
            audios: list[str] = persona_info.get_audio_url()
            videos: list[str] = persona_info.get_video_url()

            images_list: list[list[str]] = [images]
            audios_list: list[list[str]] = [audios]
            videos_list: list[list[str]] = [videos]
            
            reply_msgs = persona_info.from_reference_chain()
            reply_msgs_texts: list[str] = []
            async for msg in reply_msgs:
                if msg.is_self:
                    break

                forward_msgs_text = await self.parse_forward_msgs(msg, send_msg)
                if forward_msgs_text:
                    reply_msgs_texts.append(forward_msgs_text)
                reply_msgs_texts.append(msg.message_striped_str)
                reply_msgs_images: list[str] = await msg.get_images_url()
                reply_msgs_audios: list[str] = msg.get_audio_url()
                reply_msgs_videos: list[str] = msg.get_video_url()

                images_list.append(reply_msgs_images)
                audios_list.append(reply_msgs_audios)
                videos_list.append(reply_msgs_videos)

            reply_msgs_text = "\n\n".join(reversed(reply_msgs_texts))
            reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")

            if reply_msgs_text:
                if message_text:
                    message_text = f"Reply messages:\n{reply_msgs_text}\n\n---\n\n{message_text}"
                else:
                    message_text = reply_msgs_text
            
            # 恢复消息顺序
            images = list(chain.from_iterable(reversed(images_list)))
            audios = list(chain.from_iterable(reversed(audios_list)))
            videos = list(chain.from_iterable(reversed(videos_list)))

            if not images:
                if not message_text:
                    message = str(message)
            
            return Message(
                text = message_text,
                images = images,
                audios = audios,
                videos = videos
            )

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message {message} from {namespace}",
            message = persona_info.message_striped_str,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )
        
        client = self.get_client(persona_info)

        message = await self.parse_message(persona_info, send_msg)

        response = await self.send_message(
            client = client,
            images = message.images,
            audios = message.audios,
            videos = message.videos,
            message = message.text,
            persona_info = persona_info,
            send_msg = send_msg
        )
        
        chat_send_msg = ChatSendMsg(
            component = send_msg.component,
            persona_info = persona_info,
            matcher = send_msg.matcher,
            response = response,
            reasoning_content_handler = self.reason_filters,
            content_handler = self.filters
        )
        await self.send_chat_send_msg(chat_send_msg)
    
    def filters(self, text: str) -> str:
        return text
    
    def reason_filters(self, text: str) -> str:
        return text
    
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
    ) -> Response[ChatResponse]:
        response: Response[ChatResponse] = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
        )
        return response
    
    async def send_chat_send_msg(self, chat_send_msg: ChatSendMsg) -> NoReturn:
        await chat_send_msg.send()