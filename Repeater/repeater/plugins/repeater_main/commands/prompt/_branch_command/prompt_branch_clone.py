from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import CloneBranch
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

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)