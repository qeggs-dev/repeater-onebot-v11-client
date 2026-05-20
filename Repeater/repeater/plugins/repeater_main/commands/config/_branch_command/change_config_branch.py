from ....assist import PersonaInfo
from ....command_register import CommandCaller, CmdType
from ..._bases import ChangeBranch
from ..._clients import ConfigClient


@CommandCaller.register
class ChangeConfigBranch(ChangeBranch):
    cmd = "changeConfigBranch"
    aliases = {
        "ccfgb",
        "CCFGB",
        "change_config_branch",
        "Change_Config_Branch",
        "ChangeConfigBranch",
        "CHANGE_CONFIG_BRANCH",
    }
    cmd_type = CmdType.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)