import httpx
import orjson
from ....logger import logger as base_logger

from ....client_net_configs import *
from ....assist import http_transport
from ....exit_register import ExitRegister
from ._request_log_object import RequestLog

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class RequestLogClient:
    _client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.request_log,
        transport = http_transport
    )
    
    async def get_request_log(self):
        async with self._client.stream(
            "GET",
            REQUEST_LOG_STREAM_ROUTE
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_lines():
                chunk_data = orjson.loads(chunk)
                yield RequestLog(**chunk_data)

    # region close
    def close(self) -> None:
        self._client.aclose()
    # endregion