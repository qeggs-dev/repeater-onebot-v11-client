from dataclasses import dataclass
from types import TracebackType

@dataclass
class ExceptionInfo:
    exc_type: type[BaseException] | None = None
    exc_value: BaseException | None = None
    exc_traceback: TracebackType | None = None

    def __bool__(self) -> bool:
        return self.exc_type is not None and self.exc_value is not None and self.exc_traceback is not None