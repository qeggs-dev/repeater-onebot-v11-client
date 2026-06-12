import httpx
from uuid import UUID

from ...assist import http_transport
from ...client_net_configs import *
from ...assist import Response, PersonaInfo, CmdTypes
from ._nexus_response import (
    NexusUploadResponse,
    NexusDownloadResponse
)
from ...logger import logger as base_logger

logger = base_logger.bind(module = "UserData.Core")

class NexusClient:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.data_manager,
        transport = http_transport
    )

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    # region upload to nexus
    async def upload_to_nexus(self, timeout: int | None = None) -> Response[NexusUploadResponse]:
        response = await self._httpx_client.post(
            f"/nexus/upload/{self._info.namespace_str}/environment",
            json = {
                "timeout": timeout
            }
        )
        return Response(
            httpx_response = response,
            model = NexusUploadResponse
        )
    # endregion
    
    # region download from nexus
    async def download_from_nexus(self, uuid: str) -> Response[NexusDownloadResponse]:
        try:
            uuid = UUID(uuid)
        except ValueError:
            raise ValueError("UUID is not valid")
        
        response = await self._httpx_client.post(
            f"/nexus/download/{self._info.namespace_str}/environment",
            json = {
                "id": str(uuid)
            }
        )
        return Response(
            httpx_response = response,
            model = NexusDownloadResponse
        )
    # endregion

    # region close
    def close(self) -> None:
        self._httpx_client.aclose()
    # endregion