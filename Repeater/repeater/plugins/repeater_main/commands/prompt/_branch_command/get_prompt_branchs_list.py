from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import GetBranchList, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class GetPromptBranchsList(GetBranchList):
    cmd = "getPromptBranchList"
    aliases = {
        "gpbl",
        "GPBL",
        "get_prompt_branchs_list",
        "Get_Prompt_Branchs_List",
        "GetPromptBranchsList",
        "GET_PROMPT_BRANCHS_LIST",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT