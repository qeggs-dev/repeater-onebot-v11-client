import httpx
from typing import (
    Any
)

from ....client_net_configs import *
from ....assist import PersonaInfo, Response, http_transport, get_ssl_context
from ....logger import logger
from ...._adaptation_info import __adaptation__, __adaptation_text__

class TemplateRenderClient:
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.variable_expansion,
        transport = http_transport,
        verify = get_ssl_context()
    )

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    def _add_extra_template_fields(self, extra_template_fields: dict[str, Any] | None = None) -> dict[str, Any]:
        if extra_template_fields is None:
            extra_template_fields = {}
        extra_template_fields.update(
            {
                "message_type": self._info.source.value,
                "adaptation_version": __adaptation__,
                "adaptation_info": __adaptation_text__,
            }
        )
    
    # region set note  
    async def render(self, text: str, **extra_fields: Any) -> Response[None]:
        logger.info("Expanding variable", module = "variable_expansion.core")
        self._add_extra_template_fields(extra_fields)
        response = await self._httpx_client.post(
            f"{TEMPLATE_RENDER}/{self._info.namespace_str}",
            json={
                "user_info":{
                    "username": self._info.nickname,
                    "nickname": self._info.display_name,
                    "gender": self._info.gender,
                    "age": self._info.age,
                },
                "text": text,
                "extra_fields": extra_fields
            }
        )
        return Response(
            response
        )
    # endregion