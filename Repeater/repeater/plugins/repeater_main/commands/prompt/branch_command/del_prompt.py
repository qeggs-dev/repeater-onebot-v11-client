from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import DeleteBranch, UserdataCmdsType
from ....clients import PromptClient


@CommandCaller.register
class DeletePrompt(DeleteBranch):
    cmd = "deletePrompt"
    aliases = {
        "dp",
        "DP",
        "delete_prompt",
        "Delete_Prompt",
        "DeletePrompt",
        "DELETE_PROMPT",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT