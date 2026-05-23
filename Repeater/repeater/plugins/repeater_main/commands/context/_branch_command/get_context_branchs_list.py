from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CmdTypes
from ..._bases import GetBranchList, BranchType
from ..._clients import ContextClient


@CommandCaller.register
class GetContextBranchsList(GetBranchList):
    cmd = "getContextBranchsList"
    aliases = {
        "gcbl",
        "GCBL",
        "get_context_branchs_list",
        "Get_Context_Branchs_List",
        "GetContextBranchsList",
        "GET_CONTEXT_BRANCHS_LIST",
    }
    cmd_type = CmdTypes.BRANCH_CONTEXT

    def get_client(self, persona_info: PersonaInfo) -> ContextClient:
        return ContextClient(persona_info)