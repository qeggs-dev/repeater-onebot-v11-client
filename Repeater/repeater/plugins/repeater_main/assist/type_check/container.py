from typing import TypeVar, Container, Any, TypeGuard

T = TypeVar("T")

def is_container(obj: Container[T] | Any) -> TypeGuard[Container[T]]:
    if hasattr(obj, "__contains__"):
        return True
    return False