import json
import httpx
from typing import (
    Optional,
    Union
)

from ...client_net_configs import *
from ...assist import Response, BaseClient
from .version_model import VersionModel

class VersionAPIClient(BaseClient):
    timeout = storage_configs.server_api_timeout.version

    async def get_version(self) -> Response[VersionModel]:
        response = await self.client.get(
            url = VERSION_ROUTE,
        )
        return Response(
            httpx_response = response,
            model = VersionModel
        )