import re

from ...assist import PersonaInfo, SendMsg, Response
from .._clients import ChatClient, ChatResponse, ChatSendMsg
from ...command_register import CmdTypes
from .base_chat_pkg import BaseChat, Message
from typing import ClassVar
from ...logger import logger

class BaseFIM(BaseChat):
    echo: ClassVar[bool | None] = None
    cmd_type = CmdTypes.FIM

    fim_regex = re.compile(r"^(?P<prompt>.*?)\[fill_this\](?P<suffix>.*)$", re.IGNORECASE | re.DOTALL)
    fim_regex_greedy = re.compile(r"^(?P<prompt>.*)___(?P<suffix>.*)$", re.IGNORECASE | re.DOTALL)

    async def parse_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Message:
        if self.echo:
            text = persona_info.message_striped_str
        else:
            msg = persona_info.message_striped_str
            match_fim = self.fim_regex.match(msg)
            if match_fim:
                text = match_fim.group("prompt")
                suffix = match_fim.group("suffix")
                
                assert isinstance(text, str), "text must be a string"
                assert isinstance(suffix, str), "suffix must be a string"
                
                return Message(text=text, suffix=suffix)
            else:
                match_fim_greedy = self.fim_regex_greedy.match(msg)
                if match_fim_greedy:
                    text = match_fim_greedy.group("prompt")
                    suffix = match_fim_greedy.group("suffix")

                    assert isinstance(text, str), "text must be a string"
                    assert isinstance(suffix, str), "suffix must be a string"
                    
                    return Message(text=text, suffix=suffix)
                else:
                    await send_msg.send_error("Invalid FIM format")

        return Message(text=text)

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
            suffix = message.suffix,
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
    
    async def send_message(
        self,
        client: ChatClient,
        images: list[str],
        audios: list[str],
        videos: list[str],
        message: str,
        suffix: str | None,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        response: Response[ChatResponse] = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
            suffix = suffix,
            echo = self.echo,
            fim_mode = True
        )
        return response