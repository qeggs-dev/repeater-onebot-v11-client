from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.exception import FinishedException

from ._text_render import RendedImage
from ..core_net_configs import RepeaterDebugMode, storage_configs
from ._http_code import HTTP_Code
from ._persona_info import PersonaInfo
from ._namespace import MessageSource
from ._text_render import TextRender
from ._response import Response
from ._error_response import ErrorResponse
from ..chattts import ChatTTSAPI
from typing import (
    Callable,
    Any,
    NoReturn,
    TypeVar,
    Type,
    Literal,
    ClassVar
)
from datetime import datetime
from ._limit_speed import LimitSpeed
from ..logger import logger

T_RESPONSE = TypeVar("T_RESPONSE")

class SendMsg:
    limit_speed: ClassVar[LimitSpeed] = LimitSpeed(
        storage_configs.camouflage.send_msg_limit_speed_per_minute
    )
    def __init__(
            self,
            component: str,
            matcher: Type[Matcher],
            persona_info: PersonaInfo,
        ):
        self._component: str = component
        self._persona_info: PersonaInfo = persona_info
        self._matcher: Type[Matcher] = matcher
        self._text_render = TextRender(
            namespace = self._persona_info.namespace,
            timeout = storage_configs.server_api_timeout.render
        )
        self._prefix: Message = Message()
        self._chat_tts_api = ChatTTSAPI()
    
    def add_prefix(self, prefix: MessageSegment | str):
        self._prefix.append(prefix)
    
    def clear_prefix(self):
        self._prefix = Message()
    
    @property
    def is_debug_mode(self) -> bool:
        return RepeaterDebugMode
    
    @property
    def persona_info(self) -> PersonaInfo:
        return self._persona_info
    
    @property
    def matcher(self) -> Type[Matcher]:
        return self._matcher
    
    @property
    def component(self) -> str:
        return self._component
    
    @property
    def hello_content(self) -> str:
        now = datetime.now()
        if len(storage_configs.welcome_messages_by_weekday) == 0:
            return storage_configs.hello_content
        weekday = now.weekday() + 1
        weekday_str = now.strftime("%A")
        weekday_abridge = now.strftime("%a")
        if weekday in storage_configs.welcome_messages_by_weekday:
            return storage_configs.welcome_messages_by_weekday[weekday]
        elif str(weekday) in storage_configs.welcome_messages_by_weekday:
            return storage_configs.welcome_messages_by_weekday[str(weekday)]
        elif weekday_str in storage_configs.welcome_messages_by_weekday:
            return storage_configs.welcome_messages_by_weekday[weekday_str]
        elif weekday_abridge in storage_configs.welcome_messages_by_weekday:
            return storage_configs.welcome_messages_by_weekday[weekday_abridge]
        else:
            return storage_configs.hello_content
    
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
        :param component: 组件名称
        :param message_handler: 自定义消息文本解析处理函数
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        if callable(message):
            message = message(response)
        elif isinstance(message, str):
            message = message
        else:
            message = response.text
        await self.send_prompt(
            (
                f"{message}\n"
                f"HTTP Code: {response.code}({HTTP_Code(response.code)})"
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
        text_buffer: list[str] = []
        failed: int = 0
        for index, response in enumerate(responses, start=1):
            if isinstance(response, tuple):
                text_buffer.append(f"[{response[1]}] HTTP Code: {response[0].code}({HTTP_Code(response[0].code)})")
                if response[0].code != 200:
                    failed += 1
            elif isinstance(response, Response):
                text_buffer.append(f"[{index}] HTTP Code: {response.code}({HTTP_Code(response.code)})")
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
        await self.send_text(
            self.hello_content,
            reply = reply,
            continue_handler = continue_handler
        )
    
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
        message = Message()
        for msg in messages:
            if isinstance(msg, str):
                message.append(
                    await self.render_text(
                        msg,
                        document_bottom_comment = document_bottom_comment
                    )
                )
            elif isinstance(msg, Message):
                message.append(
                    await self.render_text(
                        msg.extract_plain_text(),
                        document_bottom_comment = document_bottom_comment
                    )
                )
        
        await self._send(
            message,
            reply = reply,
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
        await self._send(
            message,
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def break_handler(self) -> NoReturn:
        """
        跳出当前处理函数
        """
        raise FinishedException

    async def render_text(self, text: str, direct_output: bool = False, document_bottom_comment: str = "") -> MessageSegment:
        """
        渲染文本

        :param text: 渲染文本内容
        """
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
        await self.limit_speed.submit(
            self._matcher.send(send_msg)
        )
        logger.info(
            "Send message: \n{message}",
            message = send_msg
        )
        if not continue_handler:
            logger.info(
                "Break handler"
            )
            await self.break_handler()
    
    @staticmethod
    def text_length_score(text: str) -> float:
        if not text:
            return 0.0
        
        config = storage_configs.text_length_score_configs
        
        # 单次遍历统计
        max_line_length: int = 0
        total_chars_in_lines: int = 0  # 所有行中非换行符字符总数
        line_count: int = 0
        current_line_length: int = 0
        
        for char in text:
            if char == "\n":
                # 当前行结束
                if current_line_length > max_line_length:
                    max_line_length = current_line_length
                total_chars_in_lines += current_line_length
                line_count += 1
                current_line_length = 0
            else:
                current_line_length += 1
        
        # 处理最后一行（如果文本不以换行符结尾）
        if current_line_length > 0 or (text and text[-1] == '\n'):
            # 两种情况：
            # 1. current_line_length > 0: 最后有内容
            # 2. text[-1] == '\n': 最后是空行（current_line_length=0但算一行）
            if current_line_length > max_line_length:
                max_line_length = current_line_length
            total_chars_in_lines += current_line_length
            line_count += 1
        
        # 如果line_count为0（理论上不会发生，因为text不为空）
        if line_count == 0:
            return 0.0
        
        # 计算统计值
        mean_line_length: float = total_chars_in_lines / line_count
        total_length: int = len(text)  # 直接使用len，避免重复计算
        
        # 计算各项得分
        lines_score: float = line_count / config.max_lines
        max_single_line_score: float = max_line_length / config.single_line_max
        mean_line_score: float = mean_line_length / config.mean_line_max
        total_length_score: float = total_length / config.total_length
        
        # 综合得分（加权平均）
        return (
            lines_score +
            (
                max_single_line_score
                +
                mean_line_score
            ) / 2.0 +
            total_length_score
        ) / 3.0
    
    @property
    def text_length_score_threshold(self) -> float:
        if self._persona_info.source == MessageSource.GROUP:
            threshold = storage_configs.text_length_score_configs.threshold.group
        else:
            threshold = storage_configs.text_length_score_configs.threshold.private

        return threshold