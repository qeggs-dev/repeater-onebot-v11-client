from abc import abstractmethod

from ....clients import UserDataClient
from ....assist import PersonaInfo, SendMsg, CmdTypes
from ....command_register import CommandPackage

class BaseNexus(CommandPackage):
    cmd_type = CmdTypes.NEXUS
    
    @abstractmethod
    def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        pass