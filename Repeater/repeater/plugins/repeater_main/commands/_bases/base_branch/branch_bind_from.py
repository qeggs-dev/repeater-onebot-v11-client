from ....assist import PersonaInfo, SendMsg, CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class BindBranchFrom(BaseBranch):
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.bind_from(branch_id)
        await send_msg.send_response_check_code(response, f"Branch {branch_id} has been bound to the current branch.")