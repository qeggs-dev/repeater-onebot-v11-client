import httpx
from urllib.parse import quote
from ....logger import logger as base_logger
from typing import (
    Any,
)

from ....client_net_configs import *
from ....assist import Response, http_transport
from ....exit_register import ExitRegister
from ._models import (
    ModelsResponse,
    PingProviderResponse
)

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ModelInfoClient:
    _client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.model_info,
        transport = http_transport
    )
    
    # region get all models
    async def get_all_models(self) -> Response[ModelsResponse]:
        response = await self._client.get(
            f"{GET_MODEL_LIST}",
        )
        return Response(
            httpx_response = response,
            model = ModelsResponse,
        )
    # endregion

    # region get models
    async def get_models(self, model_uid: str) -> Response[ModelsResponse]:
        response = await self._client.get(
            f"{GET_MODEL_LIST}/{quote(model_uid)}",
        )
        return Response(
            httpx_response = response,
            model = ModelsResponse,
        )
    # endregion

    # region ping provider
    async def ping_provider(
            self,
            user_id: str,
            model_id: str | list[str] | None = None,
            timeout: float = 5.0,
            times: int = 4,
            size: int = 32,
            interval: int = 0
        ) -> Response[PingProviderResponse]:
        response = await self._client.post(
            f"{PING_PROVIDER}/{quote(user_id)}",
            json = {
                "model_id": model_id,
                "timeout": timeout, 
                "times": times, 
                "size": size,
                "interval": interval
            }
        )
        return Response(
            httpx_response = response,
            model = PingProviderResponse,
        )

    # region close
    def close(self) -> None:
        self._client.aclose()
    # endregion