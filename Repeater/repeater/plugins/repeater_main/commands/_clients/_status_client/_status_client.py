import httpx

from ....client_net_configs import *
from ....assist import Response, HTTPTransport, get_ssl_context
from ._response import StatusResponse

class StatusClient:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.status,
        transport = HTTPTransport(),
        verify = get_ssl_context()
    )

    async def get_client_task_status(self, namespace: str) -> Response[StatusResponse]:
        response = await self._httpx_client.get(
            url = f"/status/core/task/{namespace}",
        )
        return Response(
            httpx_response = response,
            model = StatusResponse
        )