from uuid import UUID

from ...client_net_configs import *
from ._nexus_response import (
    NexusUploadResponse,
    NexusDownloadResponse
)
from ...assist import Response, BaseClient
from ...logger import logger as base_logger

logger = base_logger.bind(module = "UserData.Core")

class NexusClient(BaseClient):
    timeout = storage_configs.server_api_timeout.data_manager
    
    # region upload to nexus
    async def upload_to_nexus(self, timeout: int | None = None) -> Response[NexusUploadResponse]:
        response = await self.client.post(
            f"/nexus/upload/{self._persona_info.namespace_str}/environment",
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
            resource_uuid = UUID(uuid)
        except ValueError:
            raise ValueError("UUID is not valid")
        
        response = await self.client.post(
            f"/nexus/download/{self._persona_info.namespace_str}/environment",
            json = {
                "id": str(resource_uuid)
            }
        )
        return Response(
            httpx_response = response,
            model = NexusDownloadResponse
        )
    # endregion