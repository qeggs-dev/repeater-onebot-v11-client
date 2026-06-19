from ....clients import UserDataClient, ContextClient, PromptClient, ConfigClient
from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandPackage
from ..userdata_cmds_type import UserdataCmdsType

class BaseNexus(CommandPackage):
    cmd_type = CmdTypes.NEXUS
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.NONE
    
    async def get_client(self, persona_info: PersonaInfo) -> UserDataClient:
        user_configs = await persona_info.get_user_configs()
        match self.userdata_cmds_type:
            case UserdataCmdsType.CONTEXT:
                return ContextClient(persona_info, user_configs)
            case UserdataCmdsType.PROMPT:
                return PromptClient(persona_info, user_configs)
            case UserdataCmdsType.CONFIG:
                return ConfigClient(persona_info, user_configs)
            case _:
                raise ValueError("Invalid userdata_cmds_type")