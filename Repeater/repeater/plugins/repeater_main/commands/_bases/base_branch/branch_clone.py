from ....assist import PersonaInfo, SendMsg, CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class CloneBranch(BaseBranch):
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.clone(branch_id)
        await send_msg.send_response_check_code(response, f"The current branch has been cloned into Branch {branch_id}.")