from ....assist import PersonaInfo, SendMsg, CmdTypes
from ....command_register import CommandCaller
from ..._bases import BindBranchFrom
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

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)