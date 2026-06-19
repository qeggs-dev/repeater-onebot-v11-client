from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import GetBranchList, UserdataCmdsType

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
    cmd_type = CmdTypes.BRANCH_CONFIG
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG