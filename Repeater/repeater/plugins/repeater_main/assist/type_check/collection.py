from typing import TypeVar, Collection, Any, TypeGuard

T = TypeVar("T")

def is_collection(obj: Collection[T] | Any) -> TypeGuard[Collection[T]]:
    if (
        hasattr(obj, "__iter__") and
        hasattr(obj, "__len__") and
        hasattr(obj, "__contains__")
    ):
        return True
    return False