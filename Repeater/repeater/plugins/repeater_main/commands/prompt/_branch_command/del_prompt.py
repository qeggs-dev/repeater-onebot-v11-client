from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import DeleteBranch
from ..._clients import PromptClient


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
    cmd_type = CmdType.BRANCH_PROMPT

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)