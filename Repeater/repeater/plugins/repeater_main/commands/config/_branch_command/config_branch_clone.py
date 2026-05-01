from ....assist import PersonaInfo
from ....command_register import CommandCaller
from ..._bases import CloneBranch
from ..._clients import ConfigClient


@CommandCaller.register
class ConfigBranchClone(CloneBranch):
    cmd = "configBranchClone"
    aliases = {
        "cfgbc",
        "CFGBC",
        "config_branch_clone",
        "Config_Branch_Clone",
        "ConfigBranchClone",
        "CONFIG_BRANCH_CLONE",
    }

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)