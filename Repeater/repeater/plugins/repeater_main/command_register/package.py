from abc import ABC, abstractmethod

from ..assist import PersonaInfo, SendMsg
from .listen_type import ListenType
from datetime import datetime, timedelta
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.typing import T_RuleChecker, T_PermissionChecker, T_State, T_Handler
from nonebot.rule import Rule
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.exception import NoneBotException
from nonebot import logger
from typing import Any, Iterable, Type, TypeVar, Generic

T = TypeVar("T")

class CommandPackage(ABC, Generic[T]):
    """
    Command Package Base Class
    """

    cmd: str | tuple[str, ...]
    """[Command Only] Command"""

    listen_type: ListenType = ListenType.Command
    """Listen Type (Command or Message)"""

    rule: T_RuleChecker | Rule | None = None
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

    component: str = None
    """The human-readable name of the Handler (required) """

    enabled: bool = True
    """Whether the handler."""

    empty_handler: bool = False
    """Whether the Handler is empty (you can not use any of the hooks in the package after setting it) """

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
        else:
            logger.exception(f"Error: {exception}")
            await send_msg.send_error(exception)
    
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
        if self.component is None:
            raise ValueError(f"{self.__class__.__name__}: Component is None")
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
        You may want to do something when you complete the registration process, overriding this method allows you to perform the task at the end of the registration.

        :return: None
        """
        pass