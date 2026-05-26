from enum import StrEnum

class SendMsgLimitType(StrEnum):
    DIRECT = "direct"
    QUEUE = "queue"