from abc import abstractmethod
from nonebot.rule import to_me
from typing import Any, TypeVar

from .._clients import ConfigClient
from ...assist import PersonaInfo, SendMsg, Response
from ...command_register import CommandPackage
from enum import Enum, auto

T = TypeVar("T")

class OperationType(Enum):
    SET = auto()
    GET = auto()
    GET_FILE_URL = auto()

class BaseConfig(CommandPackage):
    rule = to_me()
    field: str = ""
    operation: OperationType = OperationType.SET

    @property
    def component(self) -> str:
        return f"Config.{self.__class__.__name__}"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> T:
        return persona_info.message_striped_str

    @abstractmethod
    async def finish_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        response: Response[Any] | None,
        value: T
    ) -> None:
        pass
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg) -> None:
        match self.operation:
            case OperationType.SET:
                value: T = await self.parse_value(persona_info, send_msg)
                client = ConfigClient(persona_info)
                response: Response[Any] = await client.set_config(self.field, value)
                await self.finish_message(persona_info, send_msg, response, value)
            case OperationType.GET:
                client = ConfigClient(persona_info)
                response: Response[Any] = await client.get_configs(self.field)
                await self.finish_message(persona_info, send_msg, response, None)
            case OperationType.GET_FILE_URL:
                client = ConfigClient(persona_info)
                url = client.get_configs_url()
                await self.finish_message(persona_info, send_msg, None, url)