from nonebot.adapters.onebot.v11 import Message
from nonebot.internal.matcher.matcher import Matcher
from typing import NoReturn, Type, Callable
from pydantic import ValidationError

from ....assist import PersonaInfo, Response, SendMsg
from ._response_body import ChatResponse
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
            try:
                self._data = self._response.get_data()
            except ValidationError:
                self._data = None
            self._error = self._response.to_error()
        else:
            self._data = None
            self._error = None
    
    @property
    def reasoning_content(self) -> str | None:
        if self._data.reasoning_content is not None:
            return self._reasoning_content_handler(self._data.reasoning_content)
        return None

    @property
    def content(self) -> str | None:
        if self._data.content is not None:
            return self._content_handler(self._data.content)
        return None
    
    async def _send_error_message(self) -> NoReturn:
        if self._data is None:
            await self.send_response(
                self._response
            )
        else:
            await self.send_response(
                self._response,
                message = self.content
            )
    
    async def _check_response(self) -> None | NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        
        if self._error is not None:
            await self.send_error_response(self._error)
        
        if self._response.exception_info:
            await self.send_error(self._response.exception_info.exc_value)
    
    def _get_response_usage(self) -> str:
        if self._data is None:
            return ""
        return self._data.request_statistics
            

    async def send(self) -> NoReturn:
        self._check_response()

        if self._response.code == 200:
            score = self.text_length_score(self.content)
            threshold = self.text_length_score_threshold
            logger.info(f"Response content socre: {score}")
            if score >= threshold:
                logger.warning(f"Response content socre to high: {score}, Expected to be below {threshold} ")
                logger.warning("The text will be rendered as an image output.")
                await self.send_image_mode()
            else:
                await self.send_text_mode()
        else:
            await self.send_response(
                self._response,
                message = self.content
            )
    
    async def send_tts_mode(self, text: str | None = None) -> NoReturn:
        self._check_response()

        if self._response.code == 200:
            if self.reasoning_content:
                await self.send_render(
                    self.reasoning_content,
                    reply = True,
                    continue_handler = True
                )
            if self.content:
                await self.send_tts(
                    text or self._data.content,
                    reply = False,
                    continue_handler = False
                )
        else:
            await self.send_response(
                self._response,
                message = self.content
            )
    
    async def send_text_mode(self, text: str | None = None) -> NoReturn:
        self._check_response()
        
        if self._response.code == 200:
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
        else:
            await self.send_response(
                self._response,
                message = self.content
            )
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        self._check_response()
        
        if self._response.code == 200:
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
                        self.content or text,
                        document_bottom_comment = self._get_response_usage()
                    )
                )
            else:
                message.append("[Message is empty.]")
            await self._send(message)
        else:
            await self.send_response(
                self._response,
                message = self.content
            )