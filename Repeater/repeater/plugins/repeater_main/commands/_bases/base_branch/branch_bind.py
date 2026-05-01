from ....assist import PersonaInfo, SendMsg
from .base_branch import BaseBranch
from ..._clients import UserDataClient

class BindBranch(BaseBranch):
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.bind(branch_id)
        await send_msg.send_response_check_code(response, f"The current branch has been bound to Branch {branch_id}")