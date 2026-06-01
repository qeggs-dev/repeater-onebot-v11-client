from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ..persona_info import PersonaInfo
from ..response.response import Response
from typing import (
    Callable,
    Any,
    NoReturn,
    Coroutine,
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
            persona_info: PersonaInfo,
            matcher: Type[Matcher] | None = None,
        ): ...
    
    def add_prefix(self, prefix: MessageSegment | str):
        ...
    
    def clear_prefix(self):
        ...
    
    @overload
    def __call__(
            self,
            message: str | Message,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> Coroutine[Any, Any, NoReturn]: ...
    
    @overload
    def __call__(
            self,
            message: str | Message,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> Coroutine[Any, Any, None]: ...
    
    def __call__(
            self,
            message: str | Message,
            reply: bool = True,
            continue_handler: bool = False,
        ) -> Coroutine[Any, Any, None | NoReturn]: ...
    
    @property
    def is_debug_mode(self) -> bool:
        ...
    
    @property
    def persona_info(self) -> PersonaInfo:
        ...
    
    @property
    def matcher(self) -> Type[Matcher] | None:
        ...
    
    @matcher.setter
    def matcher(self, matcher: Type[Matcher] | None):
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
    async def send_http_status(
            self,
            http_status: int,
            message: str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_http_status(
            self,
            http_status: int,
            message: str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_http_status(
            self,
            http_status: int,
            message: str | None = None,
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
    async def send_render_prompt(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_render_prompt(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_render_prompt(
            self,
            text: str,
            document_bottom_comment: str = "",
            reply: bool = True,
            continue_handler: bool = False
        ): ...
    
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
            document_bottom_comment: str = "",
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
    
    def break_handler(self) -> NoReturn:
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
    
    async def _send_auto(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):...
    
    async def _send_to_matcher(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):...
    
    async def _send_to_api(
        self,
        message: str | Message | MessageSegment,
        *args,
        **kwargs
    ):...
    
    @staticmethod
    def text_length_score(text: str) -> float: ...
    
    @property
    def text_length_score_threshold(self) -> float: ...
    
    async def _send_file(self, url: str, file_name: str): ...
    
    async def send_file(self, url: str, file_name: str): ...