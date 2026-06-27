from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class PromptBranchBindFrom(BindBranchFrom):
    cmd = "promptBranchBindFrom"
    aliases = {
        "pbbf",
        "PBBF",
        "prompt_branch_bind_from",
        "Prompt_Branch_Bind_From",
        "PromptBranchBindFrom",
        "PROMPT_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT