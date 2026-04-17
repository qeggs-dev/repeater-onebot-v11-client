from nonebot.adapters.onebot.v11 import Message
from nonebot.internal.matcher.matcher import Matcher
from typing import NoReturn, Type, Callable
from pydantic import ValidationError

from ....assist import PersonaInfo, Response, SendMsg
from ._response_body import ChatResponse
from .._content_role import ContentRole
from ....chattts import ChatTTSAPI
from ....logger import logger as base_logger
from ....core_net_configs import storage_configs

logger = base_logger.bind(module = "Chat.SendMsg")

class ChatSendMsg(SendMsg):
    def __init__(
            self,
            component: str,
            persona_info: PersonaInfo,
            matcher: Type[Matcher],
            response: Response[ChatResponse],
            reasoning_content_handler: Callable[[str], str] = lambda t: t,
            content_handler: Callable[[str], str] = lambda t: t
        ):
        super().__init__(component, matcher, persona_info)
        self._response: Response[ChatResponse] = response
        self._chat_tts_api = ChatTTSAPI()
        self._reasoning_content_handler = reasoning_content_handler
        self._content_handler = content_handler
        if self._response.initialized:
            self._data = self._response.get_data()
            self._error = self._response.to_error()
        else:
            self._data = None
            self._error = None
    
    @property
    def reasoning_content(self) -> str | None:
        if self._data is None:
            return None
        buffer: list[str] = []
        for content in self._data.context.context_list:
            if content.role == ContentRole.ASSISTANT:
                buffer.append(content.reasoning_content)
        return self._reasoning_content_handler("\n\n---\n\n".join(buffer).strip())

    @property
    def content(self) -> str | None:
        if self._data is None:
            return None
        buffer: list[str] = []
        for content in self._data.context.context_list:
            if content.role == ContentRole.ASSISTANT:
                buffer.append(content.content)
        return self._content_handler("\n\n---\n\n".join(buffer).strip())
    
    async def _check_response(self) -> None | NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        
        if self._response.code != 200:
            await self.send_error_response(self._error)
        
        if self._response.exception_info:
            await self.send_error(self._response.exception_info.exc_value)
    
    def _get_response_usage(self) -> str:
        if self._data is None:
            return ""
        return self._data.request_statistics
    
    async def send(self) -> NoReturn:
        await self._check_response()

        score = self.text_length_score(self.content)
        threshold = self.text_length_score_threshold
        logger.info(f"Response content socre: {score}")
        if score >= threshold:
            logger.warning(f"Response content socre to high: {score}, Expected to be below {threshold} ")
            logger.warning("The text will be rendered as an image output.")
            await self.send_image_mode()
        else:
            await self.send_text_mode()
    
    async def send_tts_mode(self, text: str | None = None) -> NoReturn:
        await self._check_response()

        if self.reasoning_content:
            await self.send_render(
                self.reasoning_content,
                reply = True,
                continue_handler = True
            )
        if self.content:
            await self.send_tts(
                text or self.content,
                reply = False,
                continue_handler = False
            )
    
    async def send_text_mode(self, text: str | None = None) -> NoReturn:
        await self._check_response()
        
        message = Message()
        # 推理内容必须渲染为图片
        if self.reasoning_content:
            message.append(
                await self.render_text(
                    self.reasoning_content,
                    document_bottom_comment = self._get_response_usage()
                )
            )
        if self.content:
            message.append(text or self.content)
        else:
            message.append("[Message is empty.]")
        await self._send(message)
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        await self._check_response()
        
        message = Message()
        if self.reasoning_content:
            message.append(
                await self.render_text(
                    self.reasoning_content,
                    document_bottom_comment = self._get_response_usage()
                )
            )
        if self.content:
            message.append(
                await self.render_text(
                    text or self.content,
                    document_bottom_comment = self._get_response_usage()
                )
            )
        else:
            message.append("[Message is empty.]")
        await self._send(message)