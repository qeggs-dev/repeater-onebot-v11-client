import asyncio

from nonebot.adapters.onebot.v11 import Bot
from typing import Any, Awaitable, ClassVar
from functools import wraps
from cachetools import TTLCache
from ...client_net_configs import storage_configs
from ...logger import logger

class CachedAPI(Bot):
    cache: ClassVar[TTLCache[tuple[str, tuple], Any, float]] = TTLCache(
        maxsize = storage_configs.platform_interface_cache_size,
        ttl = storage_configs.platform_interface_cache_timeout
    )
    cache_lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    @wraps(Bot.call_api)
    async def call_api(self, api: str, **data: Any) -> Any:
        try:
            key: tuple[str, tuple] = (api, frozenset(data.items()))
            cacheable: bool = True
        except TypeError:
            cacheable = False
        
        async with self.cache_lock:
            if cacheable:
                if key in self.cache:
                    logger.info(
                        "Cache hit: {name}",
                        name = api
                    )
                    return self.cache[key]
                else:
                    logger.info(
                        "Cache miss: {name}",
                        name = api
                    )
            else:
                logger.info(
                    "Is not cacheable call: {name}",
                    name = api
                )
        
        result = await super().call_api(api, **data)

        async with self.cache_lock:
            self.cache[key] = result
        
        return result