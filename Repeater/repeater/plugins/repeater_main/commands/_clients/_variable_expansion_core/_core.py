import httpx
from typing import (
    Any
)

from ....core_net_configs import *
from ....assist import PersonaInfo, Response
from ....logger import logger

class VariableExpansionCore:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.variable_expansion
    )

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    # region set note  
    async def expand_variable(self, text: str, **extra_fields: Any) -> Response[None]:
        logger.info("Expanding variable", module = "variable_expansion.core")
        response = await self._httpx_client.post(
            f"{VARIABLE_EXPANSION}/{self._info.namespace_str}",
            json={
                "user_info":{
                    "username": self._info.nickname,
                    "nickname": self._info.display_name,
                    "gender": self._info.gender,
                    "age": self._info.age,
                },
                "text": text,
                **extra_fields
            }
        )
        return Response(
            response
        )
    # endregion