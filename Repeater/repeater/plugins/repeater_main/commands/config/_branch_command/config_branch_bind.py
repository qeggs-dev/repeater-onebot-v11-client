from ....assist import PersonaInfo
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranch
from ....clients import ConfigClient


@CommandCaller.register
class ConfigBranchBind(BindBranch):
    cmd = "configBranchBind"
    aliases = {
        "cfgbb",
        "CFGBB",
        "config_branch_bind",
        "Config_Branch_Bind",
        "ConfigBranchBind",
        "CONFIG_BRANCH_BIND",
    }
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)