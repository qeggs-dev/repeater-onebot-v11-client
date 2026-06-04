import asyncio

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.internal.matcher.matcher import Matcher
from typing import NoReturn, Type, Callable

from .....assist import PersonaInfo, Response, SendMsg
from .._response_body import ChatResponse
from ..._content_role import ContentRole
from .....assist import ChatTTSAPI
from .....logger import logger as base_logger
from .....client_net_configs import storage_configs

logger = base_logger.bind(module = "Chat.SendMsg")

class ChatSendMsg(SendMsg):
    def __init__(
            self,
            component: str,
            persona_info: PersonaInfo,
            matcher: Type[Matcher],
            response: Response[ChatResponse],
            reasoning_content_handler: Callable[[str], str] = lambda t: t,
            content_handler: Callable[[str], str] = lambda t: t,
            strip: bool = True,
        ):
        super().__init__(
            component = component,
            persona_info = persona_info,
            matcher = matcher,
        )
        self._response: Response[ChatResponse] = response
        self._chat_tts_api = ChatTTSAPI()
        self._reasoning_content_handler = reasoning_content_handler
        self._content_handler = content_handler
        self._strip = strip
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
                if content.reasoning_content and content.reasoning_content.strip():
                    buffer.append(content.reasoning_content)
        merged_content = "\n\n---\n\n".join(buffer)
        if self._strip:
            merged_content = merged_content.strip()
        return self._reasoning_content_handler(merged_content)

    @property
    def content(self) -> str | None:
        if self._data is None:
            return None
        buffer: list[str] = []
        for content in self._data.context.context_list:
            if content.role == ContentRole.ASSISTANT:
                if content.content and content.content.strip():
                    buffer.append(content.content)
            if content.role == ContentRole.TOOLS:
                if content.tool_calls:
                    for tool_call in content.tool_calls:
                        buffer.append(f"[Call Tool] {tool_call.function.name}")
        merged_content = "\n\n---\n\n".join(buffer)
        if self._strip:
            merged_content = merged_content.strip()
        return self._content_handler(merged_content)
    
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
            message.append(await self.empty_message())
        await self._send(message)
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        await self._check_response()
        tasks: list[asyncio.Task[MessageSegment]] = []

        if self.reasoning_content:
            reason_render_task = asyncio.create_task(
                self.render_text(
                    self.reasoning_content,
                    document_bottom_comment = self._get_response_usage()
                )
            )
            tasks.append(reason_render_task)
        if self.content:
            content_render_task = asyncio.create_task(
                self.render_text(
                    self.content,
                    document_bottom_comment = self._get_response_usage()
                )
            )
            tasks.append(content_render_task)
        else:
            tasks.append(
                asyncio.create_task(
                    self.empty_message()
                )
            )
        
        if tasks:
            results = await asyncio.gather(*tasks)
            message = Message(results)
            await self._send(message)
        else:
            await self.send_error("Nothing can be sent.")