from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import ChangeBranch, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class ChangePromptBranch(ChangeBranch):
    cmd = "changePromptBranch"
    aliases = {
        "cpb",
        "CPB",
        "change_prompt_branch",
        "Change_Prompt_Branch",
        "ChangePromptBranch",
        "CHANGE_PROMPT_BRANCH",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT