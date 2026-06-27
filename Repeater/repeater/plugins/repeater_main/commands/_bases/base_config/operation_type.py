from enum import Enum, auto

class OperationType(Enum):
    SET = auto()
    GET = auto()
    GET_FILE_URL = auto()
    GET_AND_SET = auto()