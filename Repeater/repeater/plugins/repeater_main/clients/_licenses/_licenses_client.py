import httpx

from ...client_net_configs import *
from ...assist import Response, BaseClient

class LicenseClient(BaseClient):
    timeout = storage_configs.server_api_timeout.licenses
    base_router = "license"

    async def get_requirement_license(self, requirement_name: str) -> Response[dict[str, str]]:
        response = await self.client.get(
            url = self.join_url_static("requirement", requirement_name),
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )

    async def get_requirement_list(self) -> Response[list[str]]:
        response = await self.client.get(
            url = "/requirement_list",
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )
    
    async def get_server_licenses(self) -> Response[dict[str, str]]:
        response = await self.client.get(
            url = "/self",
        )
        return Response(
            httpx_response = response,
            parsed_data = response.json()
        )