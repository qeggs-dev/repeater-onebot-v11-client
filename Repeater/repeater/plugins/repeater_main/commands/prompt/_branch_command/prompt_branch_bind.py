from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdType
from ..._bases import BindBranch
from ..._clients import PromptClient


@CommandCaller.register
class PromptBranchBind(BindBranch):
    cmd = "promptBranchBind"
    aliases = {
        "pbb",
        "PBB",
        "prompt_branch_bind",
        "Prompt_Branch_Bind",
        "PromptBranchBind",
        "PROMPT_BRANCH_BIND",
    }
    cmd_type = CmdType.BRANCH_PROMPT

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)