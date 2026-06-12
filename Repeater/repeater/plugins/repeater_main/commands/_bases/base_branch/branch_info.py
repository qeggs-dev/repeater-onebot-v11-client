from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from .base_branch import BaseBranch
from ....clients import UserDataClient
from .branch_type import BranchType

class BranchInfo(BaseBranch):
    branch_type: BranchType = BranchType.Reserved

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        client = self.get_client(persona_info)
        response = await client.branch_info()
        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")

            text_buffer: list[str] = []
            text_buffer.append(f"Branch Type: {self.branch_type.name}")
            text_buffer.append(f"Branch ID: {data.branch_id}")
            if data.file_exists:
                text_buffer.append(f"Branch Size: {data.size}")
                text_buffer.append(f"Branch Readable Size: {data.readable_size}")
                text_buffer.append(f"Branch Last Modified Time: {data.modified_datetime().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                text_buffer.append("Branch File Not Exists")

            await send_msg.send_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response, f"Get {self.branch_type.name} branch info failed")