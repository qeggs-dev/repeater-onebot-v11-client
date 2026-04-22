from abc import abstractmethod

from ..._clients import UserDataClient
from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandPackage

class BaseNexus(CommandPackage):

    @property
    def component(self) -> str:
        return f"Nexus.{self.__class__.__name__}"
    
    @abstractmethod
    def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        pass