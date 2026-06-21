import httpx
from typing import (
    Any
)

from ...client_net_configs import *
from ...assist import PersonaInfo, Response, BaseClient
from ...logger import logger
from ..._adaptation_info import __adaptation__, __adaptation_text__

class TemplateRenderClient(BaseClient):
    timeout = storage_configs.server_api_timeout.variable_expansion

    def __init__(self, info: PersonaInfo):
        self._info = info
    
    def _add_extra_template_fields(self, extra_template_fields: dict[str, Any] | None = None):
        if extra_template_fields is None:
            extra_template_fields = {}
        additional_fields = {
            "message_type": self._info.source.value,
            "adaptation_version": __adaptation__,
            "adaptation_info": __adaptation_text__,
        }
        merged_extra_template_fields = extra_template_fields | additional_fields
        return merged_extra_template_fields
    
    # region set note  
    async def render(self, text: str, **extra_fields: Any) -> Response[None]:
        logger.info("Expanding variable", module = "variable_expansion.core")
        merged_extra_template_fields = self._add_extra_template_fields(extra_fields)
        response = await self.client.post(
            f"{TEMPLATE_RENDER}/{self._info.namespace_str}",
            json={
                "user_info":{
                    "username": self._info.nickname,
                    "nickname": self._info.display_name,
                    "gender": self._info.gender,
                    "age": self._info.age,
                },
                "text": text,
                "extra_fields": merged_extra_template_fields
            }
        )
        return Response(
            response
        )
    # endregion