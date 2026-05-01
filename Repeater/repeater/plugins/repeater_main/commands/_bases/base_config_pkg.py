from abc import abstractmethod
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
    GET_AND_SET = auto()

class BaseConfig(CommandPackage):
    field: str = ""
    operation: OperationType = OperationType.SET

    @property
    def component(self) -> str:
        return f"Config.{self.__class__.__name__}"

    async def parse_value(self, persona_info: PersonaInfo, send_msg: SendMsg) -> T:
        return persona_info.message_striped_str
    
    async def parse_value_free(
            self,
            persona_info: PersonaInfo,
            send_msg: SendMsg,
            raw_value: Any | None = None
        ) -> tuple[str, T]:
        return self.field, await self.parse_value(persona_info, send_msg)

    @abstractmethod
    async def finish_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
        response: Response[Any] | None,
        field: str | None,
        value: T | None
    ) -> None:
        pass
    
    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg) -> None:
        client = ConfigClient(persona_info)
        raw_value = None
        if self.operation in [OperationType.GET, OperationType.GET_AND_SET]:
            response = await client.get_configs()
            if not response:
                await send_msg.send_error_response(response)
            else:
                config: dict = response.json()
                raw_value = config.get(self.field)
        
        field, value = await self.parse_value_free(
            persona_info,
            send_msg,
            raw_value
        )
        match self.operation:
            case OperationType.SET:
                response: Response[Any] = await client.set_config(field, value)
            case OperationType.GET:
                response: Response[Any] = await client.get_configs()
            case OperationType.GET_FILE_URL:
                response = None
                value = client.get_configs_url()
        
        await self.finish_message(
            persona_info = persona_info,
            send_msg = send_msg,
            response = response,
            field = field,
            value = value
        )