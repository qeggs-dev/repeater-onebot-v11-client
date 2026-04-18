import httpx
from .....logger import logger as base_logger
from typing import (
    Optional,
    Union,
    Any,
)

from .....assist import Response, PersonaInfo
# 服务端配置
from .....client_net_configs import *
from .....exit_register import ExitRegister

from .._base_user_data_client import UserDataClient

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ConfigClient(UserDataClient):
    _httpx_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.config
    )

    def __init__(self, info: PersonaInfo):
        super().__init__(info, "config")
    
    # region set config
    async def set_config(self, config_key: str, value: Any, item_type: str = "auto") -> Response[Any | None]:
        TYPES = {
            int: "int",
            float: "float",
            str: "string",
            bool: "boolean",
            dict: "dict",
            list: "list",
            None: "null"
        }
        if item_type == "raw":
            item_type = "raw"
        if item_type == "auto":
            if value is None:
                item_type = "null"
            elif type(value) not in TYPES:
                raise TypeError(f"Unsupported type: {type(value).__name__}")
            else:
                item_type = TYPES[type(value)]
        else:
            if item_type not in TYPES:
                raise TypeError(f"Unsupported type: {item_type}")
        logger.info(
            "Set config: {config_key} = {value}(type:{item_type})",
            config_key=config_key,
            value=value,
            item_type=item_type
        )
        response = await self._httpx_client.put(
            f"{SET_CONFIG_ROUTE}/{self._info.namespace_str}/{config_key}",
            json={
                "type": item_type,
                "value": value
            }
        )
        return Response(response)
    # endregion

    # region get config
    async def get_configs(self) -> Response[Any | None]:
        logger.info("Get {user} configs", user=self._info.namespace_str)
        response = await self._httpx_client.get(
            f"{GET_CONFIG_ROUTE}/{self._info.namespace_str}"
        )
        return Response(response)
    
    def get_config_url(self) -> str:
        return f"{GET_CONFIG_ROUTE}/{self._info.namespace_str}.json"
    # endregion

    # region remove config key
    async def remove_config_key(self, config_key: str) -> Response[None]:
        logger.info("Remove config key: {config_key}", config_key=config_key)
        response = await self._httpx_client.delete(
            f"{REMOVE_CONFIG_KEY_ROUTE}/{self._info.namespace_str}/{config_key}"
        )
        return Response(response)
    # endregion