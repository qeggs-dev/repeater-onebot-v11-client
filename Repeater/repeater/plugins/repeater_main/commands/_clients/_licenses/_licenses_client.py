import httpx

from ....client_net_configs import *
from ....assist import Response, HTTPTransport, get_ssl_context

class LicenseClient:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.licenses,
        transport = HTTPTransport(),
        verify = get_ssl_context()
    )

    async def get_requirement_license(self, requirement_name: str) -> Response[dict[str, str]]:
        response = await self._httpx_client.get(
            url = f"/license/requirement/{requirement_name}",
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )

    async def get_requirement_list(self) -> Response[list[str]]:
        response = await self._httpx_client.get(
            url = f"/license/requirement_list",
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )
    
    async def get_server_licenses(self) -> Response[dict[str, str]]:
        response = await self._httpx_client.get(
            url = "/license/self",
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )