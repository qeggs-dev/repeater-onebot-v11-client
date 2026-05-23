from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdTypes
from ..._bases import CloneBranchFrom
from ..._clients import PromptClient


@CommandCaller.register
class PromptBranchCloneFrom(CloneBranchFrom):
    cmd = "promptBranchCloneFrom"
    aliases = {
        "pbcf",
        "PBCF",
        "prompt_branch_clone_from",
        "Prompt_Branch_Clone_From",
        "PromptBranchCloneFrom",
        "PROMPT_BRANCH_CLONE_FROM",
    }
    cmd_type = CmdTypes.BRANCH_PROMPT

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)