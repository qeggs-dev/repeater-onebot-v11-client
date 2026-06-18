import os
import shutil
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable, Generic, TypeVar
from abc import abstractmethod
from .._sync_base_storage import SyncStorage

T_STORAGE_DATA = TypeVar("T_STORAGE_DATA")

class AsyncStorage(SyncStorage, Generic[T_STORAGE_DATA]):
    """
    Storage

    文件存储管理器
    """
    
    @abstractmethod
    async def load(self, path: str | os.PathLike) -> T_STORAGE_DATA:
        pass
    
    @abstractmethod
    async def save(self, path: str | os.PathLike, data: T_STORAGE_DATA) -> None:
        pass

    @abstractmethod
    async def load_line_stream(self, path: str | os.PathLike) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    async def load_stream(self, path: str | os.PathLike) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    async def save_stream(self, path: str | os.PathLike, data: Iterable[T_STORAGE_DATA]) -> None:
        pass

    @abstractmethod
    async def save_astream(self, path: str | os.PathLike, data: AsyncIterable[T_STORAGE_DATA]) -> None:
        pass