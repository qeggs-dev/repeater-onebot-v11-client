import httpx
import textwrap

from abc import (
    ABC,
    abstractmethod
)
from ..assist import (
    PersonaInfo,
    SendMsg
)
from .listen_type import ListenType
from .cmd_type import CmdTypes
from .exceptions import *
from datetime import (
    datetime,
    timedelta
)
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent
)
from nonebot.matcher import Matcher
from nonebot.typing import (
    T_RuleChecker,
    T_PermissionChecker,
    T_State,
    T_Handler
)
from nonebot.rule import (
    Rule,
    to_me
)
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.exception import NoneBotException
from nonebot import logger
from typing import (
    Any,
    Iterable,
    NoReturn,
    Type,
    TypeVar,
    Generic,
)

T = TypeVar("T")

class CommandPackage(ABC, Generic[T]):
    """
    Command Package Base Class
    """

    cmd: str | tuple[str, ...]
    """[Command Only] Command"""

    listen_type: ListenType = ListenType.Command
    """Listen Type (Command or Message)"""

    rule: T_RuleChecker | Rule | None = to_me()
    """Matcher Rule"""
    
    aliases: Iterable[str | tuple[str, ...]] | None = None
    """[Command Only] Command Aliases"""

    force_whitespace: str | bool | None = None
    """[Command Only] Must be followed by a specified space character."""

    permission: T_PermissionChecker | Permission | None = None
    """The permission of the event."""

    handlers: list[T_Handler | Dependent[Any]] | None = None
    """Event handlers list"""

    temp: bool = False
    """Is executed only once."""

    expire_time: datetime | timedelta | None = None
    """Cache expiration time"""

    priority: int = 1
    """Handler priority (the lower the number, the higher the priority) """

    block: bool = True
    """Whether to prevent a message from continuing to spread down after it has been hit."""

    state: T_State | None = None
    """Default state"""

    cmd_type: CmdTypes = CmdTypes.RESERVED
    """Command Type"""

    enabled: bool = True
    """Whether the handler."""

    empty_handler: bool = False
    """Whether the Handler is empty (you can not use any of the hooks in the package after setting it) """

    documents: str | list[str] | None = None
    """This handler's documentation"""

    superuser_permissions: bool = False
    """Whether the Handler is superuser permissions."""

    @property
    def component(self) -> str:
        """The human-readable name of the Handler (required) """
        return f"Repeater.{self.cmd_type.value}.{self.__class__.__name__}"
    
    @property
    def description(self) -> str:
        """Handler description"""
        
        text = ""

        if isinstance(self.documents, str):
            text = textwrap.dedent(
                self.documents.expandtabs(4)
            )
        elif isinstance(self.documents, list):
            text = "\n".join(self.documents)
        
        return text

    async def message_enter(self, bot: Bot, event: MessageEvent, matcher: Type[Matcher]) -> tuple[PersonaInfo, SendMsg]:
        """
        When you register a Message Handler, the Repeater will call this section before starting to get the abstraction layer object.
        
        You can intercept and do whatever you want here.

        :param bot: Bot object
        :param event: MessageEvent object
        :param matcher: Matcher object
        :return: PersonaInfo object, SendMsg object
        """
        persona_info = PersonaInfo.from_message(
            bot = bot,
            event = event
        )
        send_msg = SendMsg(
            component = self.component,
            persona_info = persona_info,
            matcher = matcher
        )
        return persona_info, send_msg

    async def command_enter(self, bot: Bot, event: MessageEvent, args: Message, matcher: Type[Matcher]) -> tuple[PersonaInfo, SendMsg]:
        """
        When you register a Command Handler, the Repeater will call this section before starting to get the abstraction layer object.
        
        You can intercept and do whatever you want here.

        :param bot: Bot object
        :param event: MessageEvent object
        :param args: Message object
        :param matcher: Matcher object
        :return: PersonaInfo object, SendMsg object
        """
        persona_info = PersonaInfo.from_command(
            bot = bot,
            event = event,
            args = args,
        )
        send_msg = SendMsg(
            component = self.component,
            persona_info = persona_info,
            matcher = matcher
        )
        return persona_info, send_msg
    
    async def horizontal_enter(self, persona_info: PersonaInfo, send_msg: SendMsg) -> tuple[PersonaInfo, SendMsg]:
        """
        This method is called when the call comes from another Handler other than the framework.

        :param persona_info: PersonaInfo object
        :param send_msg: SendMsg object
        :return: PersonaInfo object, SendMsg object
        """
        persona_info_copy = PersonaInfo.from_horizontal(persona_info)
        return persona_info_copy, send_msg

    @abstractmethod
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg) -> T:
        """
        Override this method to begin writing your business logic.

        :param persona_info: PersonaInfo object
        :param send_msg: SendMsg object
        """
        pass

    async def on_debug_mode(self, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        This method is executed when the Repeater discovers that the current environment configuration is Debug Mode.

        :param persona_info: PersonaInfo object
        :param send_msg: SendMsg object
        """
        await send_msg.send_debug_mode()

    async def on_error(self, exception: Exception, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        The error Handler for the Handler

        It catches all exceptions by default

        Includes all the necessary parts for the framework to work

        So you need to determine them and re-throw them to make sure the framework is working properly

        :param exception: The exception
        :param persona_info: The persona_info object
        :param send_msg: The send_msg object
        """
        if isinstance(exception, NoneBotException):
            raise
        elif isinstance(exception, RepeaterCommandException):
            if isinstance(exception, BreakWithErrorMessage):
                await send_msg.send_error(str(exception))
            elif isinstance(exception, BreakHandler) or isinstance(exception, ExitHandler):
                pass
        elif isinstance(exception, httpx.HTTPStatusError):
            await send_msg.send_http_status(
                http_status = exception.response.status_code,
                message = exception.response.text
            )
        else:
            logger.exception(f"Error: {exception}")
            await send_msg.send_error(exception)
    
    async def on_interpreter_error(self, exception: BaseException, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        This section is executed when the interpreter encounters an error that is a BaseException but not an Exception.

        You can override this method and do what you need to do.
        It is recommended to keep throwing up at this point. These exceptions probably shouldn't stop there.

        :param exception: The exception
        :param persona_info: The persona_info object
        :param send_msg: The send_msg object
        """
        logger.exception(f"Error: {exception}")
        raise
    
    async def on_cancel(self, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        This section is executed when the Handler is cancelled.

        You can override this method and do what you need to do.

        :param persona_info: The persona_info object
        :param send_msg: The send_msg object
        """
        logger.warning(f"{self.component} cancelled")
        raise
    
    async def handler_exit(self, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        This section is executed whenever the Handler fails or exits.

        You can override this method and do what you need to do.

        :param persona_info: The persona_info object
        :param send_msg: The send_msg object
        :return: None
        """
        pass
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the command package.

        Warning: this method is used for the main initialization process of the Package. Do not override this method.
        If you need advice try `__post_init__` method.
        """
        if isinstance(self.documents, str):
            self.documents = textwrap.dedent(
                self.documents.expandtabs(4)
            )
        self.__post_init__(*args, **kwargs)
    
    def __post_init__(self):
        """
        This method will be called at initialization time.
        """
        pass
    
    @classmethod
    def on_before_instantiate(cls):
        """
        You may want to do something before you instantiate it, and overriding this method can help you.

        :return: None
        """
        pass
    
    def on_registed(self):
        """
        You may want to do something when you complete the registration process,
        overriding this method allows you to perform the task at the end of the registration.

        :return: None
        """
        pass

    def on_matcher_registered(self, matcher: Type[Matcher]) -> Type[Matcher]:
        """
        You may want to do something when you complete the registration process of the matcher,
        overriding this method allows you to perform the task at the end of the registration.

        :param matcher: The matcher that has been registered.
        :return: None
        """
        return matcher

    @classmethod
    def on_reg_failed(cls, exc_type, exc_val, exc_tb):
        """
        If an error occurs during the registration of the current Handler,
        by default, the behavior of the modified method is to throw the original exception.

        :param exc_type: Exception type
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return: None
        """
        raise

    async def insufficient_access(self, persona_info: PersonaInfo, send_msg: SendMsg) -> NoReturn:
        """
        If the current user does not meet the permission requirements of the command, execute the method.
        
        :param persona_info: User information
        :param send_msg: Send message interface
        :return: None
        """
        await send_msg.send_error("Insufficient access rights.")
        await send_msg.break_handler()
    
    @classmethod
    def on_destroy(cls):
        """
        This method is executed when the current Handler is destroyed.
        Both instance and class methods are allowed.
        """
        pass
    
    @classmethod
    async def on_adestroy(cls):
        """
        The asynchronous method executes when the current Handler is destroyed.
        Both instance and class methods are allowed.
        """
        pass