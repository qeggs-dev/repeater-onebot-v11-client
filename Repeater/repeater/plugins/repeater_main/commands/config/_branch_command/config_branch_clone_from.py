from ....assist import PersonaInfo
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranchFrom
from ....clients import ConfigClient


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
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)