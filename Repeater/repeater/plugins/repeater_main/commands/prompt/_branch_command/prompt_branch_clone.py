from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import CloneBranch
from ..._clients import PromptClient


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
    cmd_type = CmdType.BRANCH_PROMPT

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)