import httpx
from urllib.parse import quote
from ....logger import logger as base_logger
from typing import (
    Any,
)

from ....client_net_configs import *
from ....assist import Response, HTTPTransport, get_ssl_context
from ....exit_register import ExitRegister
from ._models import (
    ModelsResponse,
)

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ModelInfoClient:
    _client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.model_info,
        transport = HTTPTransport(),
        verify = get_ssl_context()
    )
    
    # region get all models
    async def get_all_models(self) -> Response[ModelsResponse]:
        response = await self._client.get(
            f"{GET_MODEL_UID_LIST}",
        )
        return Response(
            httpx_response = response,
            model = ModelsResponse,
        )
    # endregion

    # region get models
    async def get_models(self, model_uid: str) -> Response[ModelsResponse]:
        response = await self._client.get(
            f"{GET_MODEL_UID_LIST}/{quote(model_uid)}",
        )
        return Response(
            httpx_response = response,
            model = ModelsResponse,
        )
    # endregion

    # region close
    def close(self) -> None:
        self._client.aclose()
    # endregion