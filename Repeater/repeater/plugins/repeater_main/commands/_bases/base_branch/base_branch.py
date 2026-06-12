from abc import abstractmethod

from ....clients import UserDataClient
from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandPackage

class BaseBranch(CommandPackage):
    cmd_type = CmdTypes.BRANCH
    
    @abstractmethod
    def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        ...
    
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        pass

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        msg = persona_info.message_striped_str

        config_client = self.get_client(persona_info)
        await self.parser(msg, config_client, send_msg)