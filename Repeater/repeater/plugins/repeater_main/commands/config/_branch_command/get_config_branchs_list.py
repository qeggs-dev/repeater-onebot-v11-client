from ....assist import PersonaInfo
from ....command_register import CommandCaller, CmdTypes
from ..._bases import GetBranchList, BranchType
from ..._clients import ConfigClient


@CommandCaller.register
class GetConfigBranchsList(GetBranchList):
    cmd = "getConfigBranchsList"
    aliases = {
        "gcfgbl",
        "GCFGBL",
        "get_config_branchs_list",
        "Get_Config_Branchs_List",
        "GetConfigBranchsList",
        "GET_CONFIG_BRANCHS_LIST",
    }
    branch_type = BranchType.Config
    cmd_type = CmdTypes.BRANCH_CONFIG

    def get_client(self, persona_info: PersonaInfo) -> ConfigClient:
        return ConfigClient(persona_info)