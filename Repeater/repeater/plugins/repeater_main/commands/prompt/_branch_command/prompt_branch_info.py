from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import CommandCaller
from ..._bases import BranchInfo, BranchType
from ....clients import PromptClient


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
    cmd_type = CmdTypes.BRANCH_PROMPT

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)