import httpx

from ...client_configs import *
from ...assist import Response, BaseClient
from ._response import StatusResponse

class StatusClient(BaseClient):
    timeout = storage_configs.server_api_timeout.status

    async def get_client_task_status(self, namespace: str) -> Response[StatusResponse]:
        response = await self.client.get(
            url = self.join_url_static("status", "core", "task", namespace),
        )
        return Response(
            httpx_response = response,
            model = StatusResponse
        )