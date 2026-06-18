import os
import shutil
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable, Generic, TypeVar
from abc import ABC, abstractmethod

T_STORAGE_DATA = TypeVar("T_STORAGE_DATA")

class SyncStorage(ABC, Generic[T_STORAGE_DATA]):
    """
    Storage

    文件存储管理器
    """
    def __init__(self, storage_base_path: str | Path):
        """
        :param storage_base_path: 存储路径
        """
        self.storage_base_path = Path(storage_base_path)
    
    def _path(self, path: str | os.PathLike):
        path = Path(path)
        if path.is_absolute():
            return path
        return self.storage_base_path / path
    
    @abstractmethod
    def load(self, path: str | os.PathLike) -> T_STORAGE_DATA:
        pass
    
    @abstractmethod
    def save(self, path: str | os.PathLike, data: T_STORAGE_DATA) -> None:
        pass

    @abstractmethod
    def load_line_stream(self, path: str | os.PathLike) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    def load_stream(self, path: str | os.PathLike) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    def save_stream(self, path: str | os.PathLike, data: Iterable[T_STORAGE_DATA]) -> None:
        pass

    def move(self, src: str | os.PathLike, dst: str | os.PathLike) -> None:
        src = self._path(src)
        dst = self._path(dst)
        src.rename(dst)
    
    def remove(self, path: str | os.PathLike) -> None:
        path = self._path(path)
        if path.exists():
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
    
    def copy(self, src: str | os.PathLike, dst: str | os.PathLike) -> None:
        src = self._path(src)
        dst = self._path(dst)
        if src.is_file():
            shutil.copy(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst)