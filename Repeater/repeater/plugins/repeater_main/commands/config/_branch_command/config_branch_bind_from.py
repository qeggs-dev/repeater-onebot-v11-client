from ....assist import PersonaInfo
from ....command_register import CommandCaller, CmdType
from ..._bases import BindBranchFrom
from ..._clients import ConfigClient


@CommandCaller.register
class ConfigBranchBindFrom(BindBranchFrom):
    cmd = "configBranchBindFrom"
    aliases = {
        "cfgbbf",
        "CFGBBF",
        "config_branch_bind_from",
        "Config_Branch_Bind_From",
        "ConfigBranchBindFrom",
        "CONFIG_BRANCH_BIND_FROM",
    }
    cmd_type = CmdType.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)