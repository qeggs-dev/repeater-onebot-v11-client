from nonebot.rule import to_me
from abc import abstractmethod

from ..._clients import UserDataClient
from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandPackage

class BaseBranch(CommandPackage):
    rule = to_me()

    @property
    def component(self) -> str:
        return f"Branch.{self.__class__.__name__}"
    
    @abstractmethod
    def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        ...
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        pass

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_striped_str

        config_client = self.get_client(persona_info)
        await self.parser(msg, config_client)