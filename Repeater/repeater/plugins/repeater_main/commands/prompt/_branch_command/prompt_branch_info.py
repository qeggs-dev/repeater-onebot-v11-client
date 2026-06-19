from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BranchInfo, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class PromptBranchInfo(BranchInfo):
    cmd = "promptBranchInfo"
    aliases = {
        "pbi",
        "PBI",
        "prompt_branch_info",
        "Prompt_Branch_Info",
        "PromptBranchInfo",
        "PROMPT_BRANCH_INFO",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT