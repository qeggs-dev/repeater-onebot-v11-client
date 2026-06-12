from ....assist import PersonaInfo, CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom
from ....clients import ConfigClient


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
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)