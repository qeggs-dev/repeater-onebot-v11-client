import os
from ._async_base_storage import BinaryStorage
from pathlib import Path
from typing import Any, AsyncGenerator, AsyncIterable, Iterable, TypeVar
import orjson
from ..logger import logger as base_logger

logger = base_logger.bind(module = "Storage.Async.Json")

T = TypeVar("T")

class OrjsonStorage(BinaryStorage):
    """
    orjson存储

    存储json数据
    """
    async def load_json(self, path: str | os.PathLike, default: T = None) -> Any | T:
        path = Path(path)
        try:
            logger.info(f"Loading json from {path.as_posix()}")
            return orjson.loads(
                await self.load(path)
            )
        except Exception as e:
            logger.error(f"Error loading json from {path.as_posix()}: {e}")
            if default is None:
                raise
            else:
                return default
    
    async def save_json(self, path: str | os.PathLike, data: Any):
        path = Path(path)
        try:
            logger.info(f"Saving json to {path.as_posix()}")
            await self.save(
                path,
                orjson.dumps(data)
            )
        except Exception as e:
            logger.error(f"Error saving json to {path.as_posix()}: {e}")
            raise
    
    async def load_jsonl(self, path: str | os.PathLike, default: T = None) -> AsyncGenerator[Any | T, None]:
        path = Path(path)
        try:
            logger.info(f"Loading jsonl from {path.as_posix()}")
            async for line in self.load_line_stream(path):
                try:
                    yield orjson.loads(line)
                except Exception as e:
                    if default is None:
                        raise
                    else:
                        yield default
        except Exception as e:
            logger.error(f"Error loading jsonl from {path.as_posix()}: {e}")
            if default is None:
                raise
            else:
                yield default
            
    async def save_jsonl(self, path: str | os.PathLike, data: Iterable[Any], append: bool = False):
        path = Path(path)
        try:
            logger.info(f"Saving jsonl to {path.as_posix()}")
            def json_dumps(obj: Iterable[Any]):
                for line in obj:
                    yield orjson.dumps(line)
                    yield b"\n"
            
            await self.save_stream(
                path,
                json_dumps(data),
                append = append
            )
        except Exception as e:
            logger.error(f"Error saving jsonl to {path.as_posix()}: {e}")
            raise
    
    async def save_jsonl_a(self, path: str | os.PathLike, data: AsyncIterable[Any], append: bool = False):
        path = Path(path)
        try:
            async def json_dumps(obj: AsyncIterable[Any]):
                async for line in obj:
                    yield orjson.dumps(line)
                    yield b"\n"
            
            await self.save_astream(
                path,
                json_dumps(data),
                append = append
            )
        except Exception as e:
            logger.error(f"Error saving jsonl to {path.as_posix()}: {e}")
            raise