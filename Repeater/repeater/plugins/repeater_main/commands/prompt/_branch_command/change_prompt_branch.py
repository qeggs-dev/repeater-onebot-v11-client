from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import ChangeBranch
from ..._clients import PromptClient


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

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)