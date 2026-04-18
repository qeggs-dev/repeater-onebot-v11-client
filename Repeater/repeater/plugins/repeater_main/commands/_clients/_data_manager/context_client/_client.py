import json
import httpx
from typing import (
    Optional,
    Union
)

from .....client_net_configs import *
from .....assist import PersonaInfo, Response
from .....logger import logger as base_logger
from ._response import (
    WithdrawResponse,
    ContextTotalLengthResponse,
    RoleStructureCheckerResponse
)
from .._base_user_data_client import UserDataClient
from ..._content_unit import ContentUnit

logger = base_logger.bind(module = "Context.Core")

class ContextClient(UserDataClient):
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.context
    )

    def __init__(self, info: PersonaInfo):
        super().__init__(info, "context")
    
    # region inject context
    async def inject_context(
            self,
            content_unit: ContentUnit,
        ) -> Response[None]:
        logger.info("Injecting {role} context", role = content_unit.role)
        response = await self._httpx_client.post(
            f"{INJECT_CONTEXT_ROUTE}/{self._info.namespace_str}",
            json = content_unit.model_dump(),
        )
        return Response(response)
    # endregion
    
    # region withdraw
    async def withdraw(self, context_pair_num: int = 1, paired: bool = True) -> Response[WithdrawResponse]:
        logger.info("Withdrawing context")
        response = await self._httpx_client.post(
            f"{WIHTDRAW_CONTEXT_ROUTE}/{self._info.namespace_str}",
            data={
                "context_pair_num": context_pair_num,
                "paired": paired
            }
        )
        return Response(
            response,
            model = WithdrawResponse
        )
    # endregion

    # region get context total length
    async def get_context_total_length(self) -> Response[ContextTotalLengthResponse]:
        logger.info("Getting context total length")
        response = await self._httpx_client.get(
            f"{GET_CONTEXT_LENGTH_ROUTE}/{self._info.namespace_str}"
        )
        return Response(
            response,
            model = ContextTotalLengthResponse
        )
    # endregion

    # region get context
    async def get_context(self) -> Response[list[ContentUnit]]:
        logger.info("Getting context")
        response = await self._httpx_client.get(
            f"{GET_CONTEXT_ROUTE}/{self._info.namespace_str}"
        )
        data = response.json()
        if isinstance(data, list):
            return Response(
                response,
                parsed_data = [ContentUnit(**data) for data in data]
            )
        else:
            return Response(response)
    
    def get_context_url(self) -> str | None:
        return f"{GET_CONTEXT_ROUTE}/{self._info.namespace_str}.json"
    # endregion

    # region check role structure
    async def check_role_structure(self) -> Response[RoleStructureCheckerResponse]:
        logger.info("Checking role structure")
        response = await self._httpx_client.get(
            f"{ROLE_STRUCTRUE_ROUTE}/{self._info.namespace_str}"
        )
        return Response(
            response,
            model = RoleStructureCheckerResponse
        )
    # endregion