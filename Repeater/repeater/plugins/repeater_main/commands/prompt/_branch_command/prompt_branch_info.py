from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import BranchInfo, BranchType
from ..._clients import PromptClient


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
    branch_type = BranchType.Prompt

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)