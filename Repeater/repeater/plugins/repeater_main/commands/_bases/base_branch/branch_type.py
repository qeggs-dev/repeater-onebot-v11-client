from enum import Enum, auto

class BranchType(Enum):
    Context = auto()
    Prompt = auto()
    Config = auto()
    Reserved = auto()