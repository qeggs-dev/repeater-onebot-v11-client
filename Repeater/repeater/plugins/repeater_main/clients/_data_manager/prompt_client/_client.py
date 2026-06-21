import httpx

from urllib.parse import urljoin
from ....client_net_configs import *
from ....assist import Response, PersonaInfo, http_transport
from ....logger import logger as base_logger
from .._base_user_data_client import UserDataClient

logger = base_logger.bind(module = "Prompt.Core")

class PromptClient(UserDataClient):
    timeout = storage_configs.server_api_timeout.prompt
    data_type = "prompt"
    
    # region set prompt  
    async def set_prompt(self, prompt: str) -> Response[None]:
        logger.info("Setting prompt")
        response = await self.client.put(
            f"{SET_PROMPT_ROUTE}/{self.namespace_str}",
            data={
                "prompt": prompt
            }
        )
        return Response(response)
    # endregion
    
    # region get prompt  
    async def get_prompt(self) -> Response[str]:
        logger.info("Getting prompt")
        response = await self.client.get(
            f"{GET_PROMPT_ROUTE}/{self.namespace_str}"
        )
        return Response(response)
    
    def get_prompt_url(self) -> str | None:
        return urljoin(self.base_url, f"{GET_PROMPT_ROUTE}/{self.namespace_str}.md")
    # endregion