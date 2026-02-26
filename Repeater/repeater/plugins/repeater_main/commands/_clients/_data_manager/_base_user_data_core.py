import json
import httpx
from abc import ABC
from uuid import UUID

from ....core_net_configs import *
from ....assist import Response, PersonaInfo
from ._nexus_response import (
    NexusUploadResponse,
    NexusDownloadResponse
)
from ....logger import logger as base_logger
from ._branch_info import BranchInfo

logger = base_logger.bind(module = "UserData.Core")

class UserDataCore(ABC):
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.data_manager,
    )

    def __init__(self, info: PersonaInfo, data_type: str):
        self._info = info
        self._data_type = data_type

    # region change subsession
    async def change_branch(self, new_branch_id: str) -> Response[None]:
        response = await self._httpx_client.put(
            f"/userdata/{self._data_type}/change/{self._info.namespace_str}",
            data={
                "new_branch_id": new_branch_id
            }
        )
        return Response(response)
    # endregion

    # region Delete
    async def delete(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f"/userdata/{self._data_type}/delete/{self._info.namespace_str}"
        )
        return Response(response)
    # endregion

    # region get branch list
    async def get_branch_list(self) -> Response[list[str]]:
        response = await self._httpx_client.get(
            f"/userdata/{self._data_type}/branchs/{self._info.namespace_str}"
        )
        return Response(response)

    # region clone
    async def clone(self, dst_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"/userdata/{self._data_type}/clone/{self._info.namespace_str}",
            data={
                "dst_branch_id": dst_branch_id
            }
        )
        return Response(response)
    # endregion

    # region clone from
    async def clone_from(self, src_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"/userdata/{self._data_type}/clone_from/{self._info.namespace_str}",
            data={
                "src_branch_id": src_branch_id
            }
        )
        return Response(response)
    # endregion

    # region bind
    async def bind(self, dst_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"/userdata/{self._data_type}/bind/{self._info.namespace_str}",
            data={
                "dst_branch_id": dst_branch_id
            }
        )
        return Response(response)
    # endregion

    # region bind from
    async def bind_from(self, src_branch_id: str) -> Response[None]:
        response = await self._httpx_client.post(
            f"/userdata/{self._data_type}/bind_from/{self._info.namespace_str}",
            data={
                "src_branch_id": src_branch_id
            }
        )
        return Response(response)
    # endregion

    # region branch info
    async def branch_info(self) -> Response[BranchInfo]:
        response = await self._httpx_client.get(
            f"/userdata/{self._data_type}/info/{self._info.namespace_str}"
        )
        return Response(
            response,
            model = BranchInfo
        )
    # endregion

    # region upload to nexus
    async def upload_to_nexus(self, timeout: int | None = None) -> Response[NexusUploadResponse]:
        response = await self._httpx_client.post(
            f"/nexus/upload/{self._info.namespace_str}/{self._data_type}",
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
            f"/nexus/download/{self._info.namespace_str}/{self._data_type}",
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