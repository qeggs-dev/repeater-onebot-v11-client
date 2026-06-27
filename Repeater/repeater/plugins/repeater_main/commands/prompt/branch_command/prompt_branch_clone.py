from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranch, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class PromptBranchClone(CloneBranch):
    cmd = "promptBranchClone"
    aliases = {
        "pbc",
        "PBC",
        "prompt_branch_clone",
        "Prompt_Branch_Clone",
        "PromptBranchClone",
        "PROMPT_BRANCH_CLONE",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT