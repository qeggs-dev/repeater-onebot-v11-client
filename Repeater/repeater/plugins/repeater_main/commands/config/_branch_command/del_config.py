from ....assist import PersonaInfo
from ....command_register import CommandCaller
from ..._bases import DeleteBranch
from ..._clients import ConfigClient


@CommandCaller.register
class DelConfig(DeleteBranch):
    cmd = "delConfig"
    aliases = {
        "dcfg",
        "DCFG",
        "delete_config",
        "Delete_Config",
        "DeleteConfig",
        "DELETE_CONFIG",
    }

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)