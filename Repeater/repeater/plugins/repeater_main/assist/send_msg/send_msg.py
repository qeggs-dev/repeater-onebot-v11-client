import time
import asyncio

from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.exception import FinishedException, ActionFailed

from ..assist_func import (
    text_length_score,
    send_group_file,
    send_private_file,
)
from ..text_render.text_render import RendedImage
from ...client_net_configs import RepeaterDebugMode, storage_configs
from ..network import HTTPCode
from ..persona_info import PersonaInfo
from ..namespace import MessageSource
from ..text_render.text_render import TextRender
from ..response.response import Response
from ..chattts import ChatTTSAPI
from typing import (
    Any,
    Callable,
    NoReturn,
    Coroutine,
    TypeVar,
    Type,
    Literal,
    ClassVar
)
from datetime import datetime
from .limit_speed import LimitSpeed
from ...logger import logger as base_logger

logger = base_logger.bind(module = "SendMsg")

T_RESPONSE = TypeVar("T_RESPONSE")

class SendMsg:
    limit_speed: ClassVar[LimitSpeed] = LimitSpeed(
        storage_configs.camouflage.send_msg_limit_speed_per_minute
    )
    def __init__(
            self,
            component: str,
            persona_info: PersonaInfo,
            matcher: Type[Matcher] | None = None,
        ):
        self._component: str = component
        self._persona_info: PersonaInfo = persona_info
        self._text_render = TextRender(
            namespace = self._persona_info.namespace,
            timeout = storage_configs.server_api_timeout.render
        )
        self._prefix: Message = Message()
        self._chat_tts_api = ChatTTSAPI()
        self._matcher: Type[Matcher] | None = matcher
        
        self._buffer: asyncio.Queue[tuple[Message, tuple, dict[str, Any], int]] = asyncio.Queue()
        self.send_to_buffer: bool = False
    
    def add_prefix(self, prefix: MessageSegment | str):
        self._prefix.append(prefix)
    
    def clear_prefix(self):
        self._prefix = Message()
    
    def __call__(
            self,
            message: str | Message,
            reply: bool = True,
            continue_handler: bool = False,
        ) -> Coroutine[Any, Any, None | NoReturn]:
        return self.send_prompt(
            message = message,
            reply = reply,
            continue_handler = continue_handler,
        )
    
    @property
    def is_debug_mode(self) -> bool:
        return RepeaterDebugMode
    
    @property
    def persona_info(self) -> PersonaInfo:
        return self._persona_info
    
    @property
    def component(self) -> str:
        return self._component
    
    @property
    def matcher(self) -> Type[Matcher] | None:
        return self._matcher
    
    @matcher.setter
    def matcher(self, matcher: Type[Matcher] | None):
        if isinstance(matcher, Matcher) or matcher is None:
            self._matcher = matcher
        else:
            raise TypeError(f"matcher must be Matcher or None, not {type(matcher).__name__}")
    
    @property
    def buffer(self) -> asyncio.Queue[tuple[Message, tuple, dict[str, Any], int]]:
        return self._buffer
    
    @buffer.setter
    def buffer(self, buffer: asyncio.Queue):
        if isinstance(buffer, asyncio.Queue):
            self._buffer = buffer
        else:
            raise TypeError(f"buffer must be asyncio.Queue, not {type(buffer).__name__}")
    
    @property
    def hello_content(self) -> str:
        now = datetime.now()
        buffer: list[str] = [
            storage_configs.hello_content
        ]

        if now.strftime("%m-%d") in storage_configs.hello_messages_for_date:
            buffer.append(
                storage_configs.hello_messages_for_date[now.strftime("%m-%d")]
            )
        
        weekday = now.weekday() + 1
        weekday_str = now.strftime("%A")
        weekday_abridge = now.strftime("%a")

        if weekday in storage_configs.hello_messages_by_weekday:
            buffer.append(
                storage_configs.hello_messages_by_weekday[weekday]
            )
        elif str(weekday) in storage_configs.hello_messages_by_weekday:
            buffer.append(
                storage_configs.hello_messages_by_weekday[str(weekday)]
            )
        elif weekday_str in storage_configs.hello_messages_by_weekday:
            buffer.append(
                storage_configs.hello_messages_by_weekday[weekday_str]
            )
        elif weekday_abridge in storage_configs.hello_messages_by_weekday:
            buffer.append(
                storage_configs.hello_messages_by_weekday[weekday_abridge]
            )

        return "".join(buffer)
    
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        用于调试模式的信息打印

        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Debug Message"
        )
        await self._send(
            self._persona_info.reply + (
                f"[{self._component}|{self._persona_info.namespace}|{self._persona_info.nickname}]: {self._persona_info.message}"
            ),
            reply = reply,
            continue_handler = continue_handler,
        )
    
    async def send_response_check_code(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        logger.info(
            "Send Response Check Code"
        )
        logger.info(
            "Response Code Is {code}",
            code = response.code
        )
        if response.code != 200:
            await self.send_error_response(
                response = response,
                message = message,
                reply = reply,
                continue_handler = continue_handler,
            )
        else:
            await self.send_response(
                response = response,
                message = message,
                reply = reply,
                continue_handler = continue_handler,
            )
    
    async def send_error_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
            logger.info(
                "Send Error Response"
            )
            if message is None:
                error = response.get_error()
                if error is not None:
                    message = f"{error.error_message}\n{error.source_exception}: {error.exception_message}"
                elif response.text:
                    message = response.text
                else:
                    message = f"[Error Info Is Invalid]"
            else:
                message = message
            
            await self.send_response(
                response,
                message,
                reply = reply,
                continue_handler = continue_handler,
            )
    
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送响应对象中的内容，主要用于HTTP错误提示

        :param response: 响应对象
        :param message_handler: 自定义消息文本或解析处理函数
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Response"
        )
        if callable(message):
            message = message(response)
        elif isinstance(message, str):
            message = message
        else:
            message = response.text
        await self.send_http_status(
            http_status = response.code,
            message = message,
            reply = reply,
            continue_handler = continue_handler,
        )
    
    async def send_http_status(
            self,
            http_status: int,
            message: str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送 HTTP 状态码，用于提示 HTTP 错误

        :param http_status: HTTP 状态码
        :param message: 消息文本
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Response"
        )
        await self.send_prompt(
            (
                f"{message}\n"
                f"HTTP Code: {http_status}({HTTPCode(http_status)})"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送多个响应对象中的内容，主要用于HTTP错误提示

        :param responses: 响应对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Multiple Responses"
        )
        text_buffer: list[str] = []
        failed: int = 0
        for index, response in enumerate(responses, start=1):
            if isinstance(response, tuple):
                text_buffer.append(f"[{response[1]}] HTTP Code: {response[0].code}({HTTPCode(response[0].code)})")
                if response[0].code != 200:
                    failed += 1
            elif isinstance(response, Response):
                text_buffer.append(f"[{index}] HTTP Code: {response.code}({HTTPCode(response.code)})")
                if response.code != 200:
                    failed += 1
            else:
                raise TypeError(f"Unsupported type: {type(response)}")
        
        if failed == 0:
            text_buffer.append("All requests are successful.")
        else:
            text_buffer.append(f"{failed} requests failed.")
        
        await self.send_prompt(
            "\n".join(text_buffer),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送欢迎信息

        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Hello Message"
        )
        hello_content = self.hello_content
        if hello_content:
            await self.send_text(
                hello_content,
                reply = reply,
                continue_handler = continue_handler
            )
        elif not continue_handler:
            self.break_handler()
    
    @property
    def prompt_str(self) -> str:
        return (
            f"==== {self._component} ====\n"
            f"> [{self._persona_info.namespace}]\n"
        )
    
    async def send_prompt(
            self,
            prompt: Message | str,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送提示信息

        :param prompt: 提示信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Prompt"
        )
        if isinstance(prompt, Message):
            await self._send(
                Message(
                    self.prompt_str,
                ).extend(prompt),
                reply = reply,
                continue_handler = continue_handler
            )
        elif isinstance(prompt, str):
            await self._send(
                self.prompt_str + prompt,
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            raise TypeError("prompt must be str or Message")
    
    async def send_error(
            self,
            error: str | Exception,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送错误信息

        :param error: 错误信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Error"
        )
        if isinstance(error, Exception):
            await self.send_prompt(
                (
                    f"{error.__class__.__name__}: {error}"
                ),
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            await self.send_prompt(
                (
                    f"Error: {error}"
                ),
                reply = reply,
                continue_handler = continue_handler
            )
    
    async def send_warning(
            self,
            warning: str,
            reply: bool = True,
            continue_handler: bool = True
        ):
        """
        发送警告信息

        :param warning: 警告信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Warning"
        )
        await self.send_prompt(
            (
                f"Warning: {warning}"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送纯文本

        :param text: 文本内容
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Text"
        )
        await self._send(
            Message(text),
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_mixed_render(
            self,
            text_to_render: str,
            text: str | None = None,
            prompt_mode: bool = False,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送混合渲染文本

        :param text: 普通文本内容
        :param text_to_render: 需要渲染的文本内容
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Mixed Render"
        )
        image = await self.render_text(
            text_to_render,
            document_bottom_comment = document_bottom_comment
        )

        if text is None:
            message = Message(
                image
            )
        else:
            message = Message(
                [
                    MessageSegment.text(text),
                    image,
                ]
            )
        
        if prompt_mode:
            await self.send_prompt(
                message,
                reply=reply,
                continue_handler = continue_handler
            )
        else:
            await self._send(
                message,
                reply=reply,
                continue_handler = continue_handler
            )
    
    async def send_multiple_render(
            self,
            messages: list[str | Message],
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> None:
        """
        发送多个渲染文本
        """
        logger.info(
            "Send Multiple Render"
        )
        tasks: list[asyncio.Task[MessageSegment]] = []
        for msg in messages:
            if isinstance(msg, str):
                tasks.append(
                    asyncio.create_task(
                        self.render_text(
                            msg,
                            document_bottom_comment = document_bottom_comment
                        )
                    )
                )
            elif isinstance(msg, Message):
                tasks.append(
                    asyncio.create_task(
                        self.render_text(
                            msg.extract_plain_text(),
                            document_bottom_comment = document_bottom_comment
                        )
                    )
                )
        
        results = await asyncio.gather(*tasks)
        message = Message(results)
        
        await self._send(
            message,
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_render_prompt(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        logger.info(
            "Send Render Prompt"
        )
        image = await self.render_text(
            text,
            document_bottom_comment = document_bottom_comment
        )
        await self._send(
            Message(
                [
                    self.prompt_str,
                    image
                ]
            ),
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_render(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送渲染后的文本

        :param text: 渲染文本内容
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Render"
        )
        image = await self.render_text(
            text,
            document_bottom_comment = document_bottom_comment
        )
        await self._send(
            Message(image),
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_tts(
            self,
            text: str,
            send_error_message: bool = True,
            reply: bool = False,
            continue_handler: bool = False
        ):
        """
        发送tts

        :param text: 文本
        :param reply: 是否回复
        :param continue_handler: 是否继续处理流程
        """
        logger.info(
            "Send TTS"
        )
        response = await self._chat_tts_api.text_to_speech(text)
        if response.code == 200:
            data = response.get_data()
            if data is not None:
                await self._send(
                    message = MessageSegment.record(data.audio_files[0].url),
                    reply = reply,
                    continue_handler = continue_handler
                )
        elif send_error_message:
            await self.send_response(response, message = "TTS Error.")
        else:
            logger.error(f"Send TTS Error: {response.code} {response.text}")
    
    async def send_check_length(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送长度检测后的文本

        :param message: 消息
        :param threshold: 长度阈值
        :param reply: 是否回复
        :param continue_handler: 是否继续处理流程
        """
        logger.info(
            "Send Check Length"
        )
        if isinstance(message, Message):
            text = message.extract_plain_text()
        elif isinstance(message, str):
            text = message
        else:
            raise TypeError(f"message must be Message or str, but got {type(message)}")
        length_score = self.text_length_score(text)
        if length_score >= threshold:
            await self.send_render(
                text,
                document_bottom_comment = document_bottom_comment,
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            await self.send_text(
                text,
                reply = reply,
                continue_handler = continue_handler
            )
    
    async def send_check_length_prompt(
            self,
            prompt: Message | str,
            threshold: float = 1.0,
            document_document_bottom_comments: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        logger.info(
            "Send Check Length Prompt"
        )
        if isinstance(prompt, Message):
            text = prompt.extract_plain_text()
        elif isinstance(prompt, str):
            text = prompt
        else:
            raise TypeError(f"message must be Message or str, but got {type(prompt)}")
        length_score = self.text_length_score(text)
        if length_score >= threshold:
            await self.send_mixed_render(
                text,
                self.prompt_str,
                document_bottom_comment = document_document_bottom_comments,
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            await self.send_prompt(
                text,
                reply = reply,
                continue_handler = continue_handler
            )
    
    @staticmethod
    async def empty_message(self) -> MessageSegment:
        return MessageSegment.text("[Message is empty.]")
    
    @staticmethod
    async def _get_text_message(content: str) -> MessageSegment:
        return MessageSegment.text(content)
    
    async def send_chat_response(
            self,
            reasoning_content: str = "",
            content: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        logger.info(
            "Send Chat Response"
        )
        tasks: list[asyncio.Task[MessageSegment]] = []
        if reasoning_content:
            tasks.append(
                asyncio.create_task(
                    self.render_text(
                        reasoning_content,
                    )
                )
            )
        
        if content:
            if self.text_length_score(content) >= self.text_length_score_threshold:
                tasks.append(
                    asyncio.create_task(
                        self.render_text(
                            content,
                        )
                    )
                )
            else:
                
                tasks.append(
                    asyncio.create_task(
                        self._get_text_message(content)
                    )
                )
        else:
            tasks.append(
                asyncio.create_task(
                    self.empty_message()
                )
            )
        
        results = await asyncio.gather(*tasks)
        message = Message(results)

        await self._send(
            message,
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_any(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送任意消息

        :param message: 消息对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        logger.info(
            "Send Any"
        )
        await self._send(
            message,
            reply=reply,
            continue_handler = continue_handler
        )
    
    def break_handler(self) -> NoReturn:
        """
        跳出当前处理函数
        """
        logger.info(
            "Break handler"
        )
        raise FinishedException

    async def render_text(self, text: str, direct_output: bool = False, document_bottom_comment: str = "") -> MessageSegment:
        """
        渲染文本

        :param text: 渲染文本内容
        """
        logger.info(
            "Render Text"
        )
        if text:
            render_response: Response[RendedImage] = await self._text_render.render(
                text,
                direct_output = direct_output,
                document_bottom_comment = document_bottom_comment
            )
            if render_response.code == 200:
                data = render_response.get_data()
                if data is not None:
                    message = MessageSegment.image(data.image_url)
                else:
                    logger.error(f"Render Data Is Invalid")
            else:
                await self.send_response(render_response, lambda response: f"Render Error: {response.text}")
            return message
        else:
            raise ValueError("Text is empty.")
    
    async def _send(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送消息

        :param message: 消息对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        send_msg = self._prefix + message
        if reply:
            send_msg = self._persona_info.reply + send_msg
        try:
            await self.limit_speed.submit(
                self._send_auto(send_msg)
            )
        except Exception as error:
            logger.error(
                "Message Send Failed: \n{error}",
                error = error
            )
            raise
        if not continue_handler:
            self.break_handler()
    
    async def _send_auto(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):
        if self.send_to_buffer:
            logger.info(
                "Send to buffer: \n{message}",
                message = message
            )
            await self._send_to_buffer()
        elif self._matcher is not None:
            logger.info(
                "Send to matcher: \n{message}",
                message = message
            )
            await self._send_to_matcher(message, *args, **kwargs)
        else:
            logger.info(
                "Send to api: \n{message}",
                message = message
            )
            await self._send_to_api(message, *args, **kwargs)
    
    async def _send_to_buffer(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):
        now = time.perf_counter_ns()
        await self._buffer.put(
            (message, args, kwargs, now)
        )
    
    async def _send_to_matcher(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):
        await self._matcher.send(message, *args, **kwargs)
    
    async def _send_to_api(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):
        bot = self._persona_info.cached_api
        if self._persona_info.source == MessageSource.GROUP:
            await bot.send_group_msg(
                group_id = self._persona_info.group_id,
                message = message,
                *args,
                **kwargs
            )
        elif self._persona_info.source == MessageSource.PRIVATE:
            await bot.send_private_msg(
                group_id = self._persona_info.user_id,
                message = message,
                *args,
                **kwargs
            )
        else:
            raise ValueError("Invalid Message Source")
    
    @staticmethod
    def text_length_score(text: str) -> float:
        return text_length_score(text)
    
    @property
    def text_length_score_threshold(self) -> float:
        if self._persona_info.source == MessageSource.GROUP:
            threshold = storage_configs.text_length_score_configs.threshold.group
        else:
            threshold = storage_configs.text_length_score_configs.threshold.private

        return threshold
    
    async def _send_file(self, url: str, file_name: str):
        try:
            if self._persona_info.source == MessageSource.GROUP:
                await send_group_file(
                    self._persona_info.cached_api,
                    self._persona_info.group_id,
                    url,
                    file_name
                )
            elif self._persona_info.source == MessageSource.PRIVATE:
                await send_private_file(
                    self._persona_info.cached_api,
                    self._persona_info.user_id,
                    url,
                    file_name
                )
        except ActionFailed as e:
            logger.error(f"Failed to upload file: {e}")
            await self.send_error("Failed to upload file.")
    
    async def send_file(self, url: str, file_name: str):
        await self.limit_speed.submit(
            self._send_file(
                url,
                file_name
            )
        )