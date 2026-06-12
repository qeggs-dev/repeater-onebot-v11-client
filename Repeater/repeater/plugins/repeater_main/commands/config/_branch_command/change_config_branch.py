from ....assist import PersonaInfo, CmdTypes
from ....command_register import CommandCaller
from ..._bases import ChangeBranch
from ....clients import ConfigClient

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
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)