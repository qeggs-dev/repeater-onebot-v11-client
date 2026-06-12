from ....assist import PersonaInfo, CmdTypes
from ....command_register import CommandCaller
from ..._bases import DeleteBranch
from ....clients import ConfigClient


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
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)