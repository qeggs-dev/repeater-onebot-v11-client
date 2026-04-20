from ....assist import PersonaInfo
from ....command_register import CommandCaller
from ..._bases import BranchInfo, BranchType
from ..._clients import ConfigClient


@CommandCaller.register
class ConfigBranchInfo(BranchInfo):
    cmd = "configBranchInfo"
    aliases = {
        "cfgbi",
        "CFGBI",
        "config_branch_info",
        "Config_Branch_Info",
        "ConfigBranchInfo",
        "CONFIG_BRANCH_INFO",
    }
    branch_type = BranchType.Config

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)