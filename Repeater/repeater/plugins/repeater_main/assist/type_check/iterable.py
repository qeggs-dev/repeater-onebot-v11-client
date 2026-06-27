from typing import Iterable, Any, TypeGuard, TypeVar

T = TypeVar("T")

def is_iterable(obj: Iterable[T] | Any) -> TypeGuard[Iterable[T]]:
    if hasattr(obj, "__iter__"):
        return True
    else:
        return False