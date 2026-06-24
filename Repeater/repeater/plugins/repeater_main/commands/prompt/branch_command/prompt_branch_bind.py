from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranch, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class PromptBranchBind(BindBranch):
    cmd = "promptBranchBind"
    aliases = {
        "pbb",
        "PBB",
        "prompt_branch_bind",
        "Prompt_Branch_Bind",
        "PromptBranchBind",
        "PROMPT_BRANCH_BIND",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT