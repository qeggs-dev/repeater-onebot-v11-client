from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient

class CloneBranchFrom(BaseBranch):
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.clone(branch_id)
        await send_msg.send_response_check_code(response, f"Branch {branch_id} has been cloned into the current branch")