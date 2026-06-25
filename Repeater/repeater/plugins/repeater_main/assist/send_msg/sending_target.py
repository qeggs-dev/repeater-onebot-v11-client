from enum import Enum, auto

class SendingTarget(Enum):
    AUTO = auto()
    MATCHER = auto()
    API = auto()
    BUFFER = auto()
    NULL = auto()