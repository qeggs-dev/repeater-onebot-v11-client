from nonebot.adapters.onebot.v11 import Message
from nonebot.internal.matcher.matcher import Matcher
from ....assist import PersonaInfo, Response, SendMsg
from ._response_body import ChatResponse
from ....chattts import ChatTTSAPI
from typing import NoReturn, Type, Callable
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
        self._data = self._response.get_data()
    
    @property
    def ai_generate_tip(self) -> str:
        return storage_configs.ai_generate_tip
    
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

    async def send(self) -> NoReturn:
        if self._response.code == 200 and self._data is not None:
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
            await self.send_error_response(self._response)
    
    async def send_tts_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._data is not None:
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
                await self.send_error_response(self._response)
    
    async def send_text_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._data is not None:
                message = Message()
                # 推理内容必须渲染为图片
                if self.reasoning_content:
                    message.append(
                        await self.render_text(
                            self.reasoning_content,
                            document_end_comments = self.ai_generate_tip
                        )
                    )
                if self.content:
                    message.append(text or self.content)
                else:
                    message.append("[Message is empty.]")
                await self._send(message)
            else:
                await self.send_error_response(self._response)
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self._response.code == 200 and self._data is not None:
                message = Message()
                if self.reasoning_content:
                    message.append(
                        await self.render_text(
                            self.reasoning_content,
                            document_end_comments = self.ai_generate_tip
                        )
                    )
                if self.content:
                    message.append(
                        await self.render_text(
                            self.content or text,
                            document_end_comments = self.ai_generate_tip
                        )
                    )
                else:
                    message.append("[Message is empty.]")
                await self._send(message)
            else:
                await self.send_error_response(self._response)