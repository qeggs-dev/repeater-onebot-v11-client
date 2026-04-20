from abc import ABC, abstractmethod

from ..assist import PersonaInfo, SendMsg
from .listen_type import ListenType
from datetime import datetime, timedelta
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.typing import T_RuleChecker, T_PermissionChecker, T_State, T_Handler
from nonebot.rule import Rule
from nonebot.permission import Permission
from nonebot.dependencies import Dependent
from nonebot.exception import NoneBotException
from typing import Any, Iterable

class CommandPackage(ABC):
    cmd: str | tuple[str, ...]
    listen_type: ListenType = ListenType.Command
    rule: T_RuleChecker | Rule | None = None
    aliases: Iterable[str | tuple[str, ...]] | None = None
    force_whitespace: str | bool | None = None
    permission: T_PermissionChecker | Permission | None = None
    handlers: list[T_Handler | Dependent[Any]] | None = None
    temp: bool = False
    expire_time: datetime | timedelta | None = None
    priority: int = 1
    block: bool = True
    state: T_State | None = None
    component: str = None
    enabled: bool = True
    empty_handler: bool = False

    @abstractmethod
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        pass

    async def on_debug_mode(self, persona_info: PersonaInfo, send_msg: SendMsg):
        await send_msg.send_debug_mode()

    async def on_error(self, exception: Exception, persona_info: PersonaInfo, send_msg: SendMsg):
        if isinstance(exception, NoneBotException):
            raise
        else:
            await send_msg.send_error(exception)
    
    def __init__(self, *args, **kwargs):
        if self.component is None:
            raise ValueError(f"{self.__class__.__name__}: Component is None")