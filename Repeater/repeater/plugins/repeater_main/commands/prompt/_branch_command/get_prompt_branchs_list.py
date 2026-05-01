from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller
from ..._bases import GetBranchList, BranchType
from ..._clients import PromptClient


@CommandCaller.register
class GetPromptBranchsList(GetBranchList):
    cmd = "getPromptBranchList"
    aliases = {
        "gpbl",
        "GPBL",
        "get_prompt_branchs_list",
        "Get_Prompt_Branchs_List",
        "GetPromptBranchsList",
        "GET_PROMPT_BRANCHS_LIST",
    }
    branch_type = BranchType.Prompt

    def get_client(self, persona_info: PersonaInfo) -> PromptClient:
        return PromptClient(persona_info)