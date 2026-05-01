from ....assist import PersonaInfo
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom
from ..._clients import ConfigClient


@CommandCaller.register
class ConfigBranchCloneFrom(CloneBranchFrom):
    cmd = "configBranchCloneFrom"
    aliases = {
        "cfgbcf",
        "CFGBCF",
        "config_branch_clone_from",
        "Config_Branch_Clone_From",
        "ConfigBranchCloneFrom",
        "CONFIG_BRANCH_CLONE_FROM",
    }

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)