import json
import httpx
from typing import (
    Optional,
    Union
)

from .....client_net_configs import *
from .....assist import Response, PersonaInfo
from .....logger import logger as base_logger
from .._base_user_data_client import UserDataClient

logger = base_logger.bind(module = "Prompt.Core")

class PromptClient(UserDataClient):
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.prompt
    )

    def __init__(self, info: PersonaInfo):
        super().__init__(info, "prompt")
    
    # region set prompt  
    async def set_prompt(self, prompt: str) -> Response[None]:
        logger.info("Setting prompt")
        response = await self._httpx_client.put(
            f"{SET_PROMPT_ROUTE}/{self._info.namespace_str}",
            data={
                "prompt": prompt
            }
        )
        return Response(response)
    # endregion
    
    # region get prompt  
    async def get_prompt(self) -> Response[str]:
        logger.info("Getting prompt")
        response = await self._httpx_client.get(
            f"{GET_PROMPT_ROUTE}/{self._info.namespace_str}"
        )
        return Response(response)
    
    def get_prompt_url(self) -> str | None:
        return f"{GET_PROMPT_ROUTE}/{self._info.namespace_str}.md"
    # endregion