from abc import abstractmethod

from ..._clients import UserDataClient
from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandPackage, CmdType

class BaseNexus(CommandPackage):
    type = CmdType.NEXUS
    
    @abstractmethod
    def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        pass