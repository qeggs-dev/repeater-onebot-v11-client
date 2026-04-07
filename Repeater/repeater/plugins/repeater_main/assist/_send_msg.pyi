from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ._persona_info import PersonaInfo
from ._response import Response
from typing import (
    Callable,
    Any,
    NoReturn,
    TypeVar,
    Type,
    overload,
    Literal
)

T_RESPONSE = TypeVar("T_RESPONSE")

class SendMsg:
    def __init__(
            self,
            component: str,
            matcher: Type[Matcher],
            persona_info: PersonaInfo,
        ): ...
    
    def add_prefix(self, prefix: MessageSegment | str):
        ...
    
    def clear_prefix(self):
        ...
    
    @property
    def is_debug_mode(self) -> bool:
        ...
    
    @property
    def persona_info(self) -> PersonaInfo:
        ...
    
    @property
    def matcher(self) -> Type[Matcher]:
        ...
    
    @property
    def component(self) -> str:
        ...
    
    @property
    def hello_content(self) -> str:
        ...
    
    @overload
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_response_check_code(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_response_check_code(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_response_check_code(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_error_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_error_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_error_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...
    
    @overload
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ): ...
    
    @overload
    async def send_prompt(
            self,
            prompt: Message | str,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_prompt(
            self,
            prompt: Message | str,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_prompt(
            self,
            prompt: Message | str,
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_error(
            self,
            error: str | Exception,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_error(
            self,
            error: str | Exception,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_error(
            self,
            error: str | Exception,
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_warning(
            self,
            warning: str,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...

    @overload
    async def send_warning(
            self,
            warning: str,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    async def send_warning(
            self,
            warning: str,
            reply: bool = True,
            continue_handler: bool = True
        ): ...
    
    @overload
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_mixed_render(
            self,
            text_to_render: str,
            text: str | None = None,
            prompt_mode: bool = False,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_mixed_render(
            self,
            text_to_render: str,
            text: str | None = None,
            prompt_mode: bool = False,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_mixed_render(
            self,
            text_to_render: str,
            text: str | None = None,
            prompt_mode: bool = False,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_multiple_render(
            self,
            messages: list[str | Message],
            document_bottom_comment: str = "",
            reply: bool = False,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...

    @overload
    async def send_multiple_render(
            self,
            messages: list[str | Message],
            document_bottom_comment: str = "",
            reply: bool = False,
            continue_handler: Literal[True] = True
        ) -> None: ...

    async def send_multiple_render(
            self,
            messages: list[str | Message],
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> None: ...
    
    @overload
    async def send_render(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    @overload
    async def send_render(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    async def send_render(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_tts(
            self,
            text: str,
            send_error_message: bool = True,
            reply: bool = False,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...

    @overload
    async def send_tts(
            self,
            text: str,
            send_error_message: bool = True,
            reply: bool = False,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_tts(
            self,
            text: str,
            send_error_message: bool = True,
            reply: bool = False,
            continue_handler: bool = False
        ):
        ...
    
    @overload
    async def send_check_length(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_check_length(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_check_length(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ):
        ...
    
    @overload
    async def send_check_length_prompt(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: bool = False,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_check_length_prompt(
            self,
            message: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_check_length_prompt(
            self,
            prompt: Message | str,
            threshold: float = 1.0,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    @overload
    async def send_any(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...

    @overload
    async def send_any(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_any(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: bool = False
        ):
        ...
    
    @overload
    async def send_chat_response(
            self,
            reasoning_content: str = "",
            content: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_chat_response(
            self,
            reasoning_content: str = "",
            content: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_chat_response(
            self,
            reasoning_content: str = "",
            content: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
    async def break_handler(self) -> NoReturn:
        ...

    async def render_text(self, text: str, direct_output: bool = False, document_bottom_comment: str = "") -> MessageSegment:
        ...
    
    @overload
    async def _send(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def _send(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def _send(
            self,
            message: str | Message | MessageSegment,
            reply: bool = True,
            continue_handler: bool = False
        ):
        ...
    
    @staticmethod
    def text_length_score(text: str) -> float: ...
    
    @property
    def text_length_score_threshold(self) -> float: ...