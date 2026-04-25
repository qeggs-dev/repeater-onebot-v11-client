import json
import httpx
from typing import (
    Optional,
    Union
)

from ....client_net_configs import *
from ....assist import Response, AsyncHTTPTransport
from .version_model import VersionModel

class VersionAPIClient:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.version,
        transport = AsyncHTTPTransport()
    )

    async def get_version(self) -> Response[VersionModel]:
        response = await self._httpx_client.get(
            url = VERSION_ROUTE,
        )
        return Response(
            httpx_response = response,
            model = VersionModel
        )