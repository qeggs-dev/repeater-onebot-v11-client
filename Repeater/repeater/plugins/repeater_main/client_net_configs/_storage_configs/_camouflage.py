from pydantic import BaseModel
from ._send_msg_limit_type import SendMsgLimitType

class Camouflage(BaseModel):
    send_msg_limit_speed_per_minute: int | float | None = 100
    send_msg_limit_type: SendMsgLimitType = SendMsgLimitType.DIRECT