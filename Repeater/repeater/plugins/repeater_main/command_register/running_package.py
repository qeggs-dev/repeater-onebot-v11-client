import asyncio
from typing import TypeVar, Generic
from .package import CommandPackage
from ..assist import PersonaInfo, SendMsg
from ..cmd_info import CmdTypes
from nonebot.matcher import Matcher
from dataclasses import dataclass

T = TypeVar("T")

@dataclass
class RunningPackage(Generic[T]):
    """
    运行中的命令包
    """
    package: CommandPackage[T]
    matcher: Matcher | None
    persona_info: PersonaInfo
    send_msg: SendMsg
    task: asyncio.Task[T]

    def __hash__(self) -> int:
        return hash((type(self), self.task))
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RunningPackage):
            return self.task == __o.task
        return False