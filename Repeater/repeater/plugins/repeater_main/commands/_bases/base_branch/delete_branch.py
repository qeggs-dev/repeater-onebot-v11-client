from abc import abstractmethod

from ....assist import PersonaInfo, SendMsg
from .base_branch import BaseBranch
from ..._clients import UserDataClient

class DeleteBranch(BaseBranch):
    async def parser(self, branch_id: str, client: UserDataClient, send_msg: SendMsg):
        response = await client.delete()
        await send_msg.send_response_check_code(response, f"Deleted active branch")