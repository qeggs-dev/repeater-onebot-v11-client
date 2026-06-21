import json
import httpx
from typing import (
    ClassVar
)

from .client_pool import (
    ClientPool,
    ClientInfo,
    ClientTimeout,
    ClientLimits
)
from ...client_net_configs import *
from ..namespace import Namespace
from ..persona_info import PersonaInfo
from ..user_config import UserConfigs

class BaseClient:
    _httpx_clients: ClassVar[ClientPool] = ClientPool(storage_configs.client_pool_size)
    follow_redirects: ClassVar[bool] = False
    timeout: ClassVar[int | float | ClientTimeout] = 5
    limits: ClassVar[ClientLimits | None] = None
    encoding: ClassVar[str] = "utf-8"

    def __init__(self, persona_info: PersonaInfo, user_configs: UserConfigs, namespace: str | Namespace | None = None):
        self._persona_info = persona_info
        self.user_configs = user_configs
        self._namespace = namespace

        client_info = ClientInfo(
            url = self.base_url,
            follow_redirects = self.follow_redirects,
            timeout = self.timeout,
            limits = self.limits,
            encoding = self.encoding
        )
        self.client = self._httpx_clients.get_client(client_info)
    
    @property
    def base_url(self) -> str:
        return self._get_backend_url(self.user_configs)
    
    @property
    def namespace(self) -> str:
        if self._namespace is not None:
            if isinstance(self._namespace, Namespace):
                return self._namespace.namespace_str
            elif isinstance(self._namespace, str):
                return self._namespace
            else:
                raise TypeError(f"Invalid type for namespace: {type(self._namespace).__name__}")
        else:
            return self._persona_info.namespace_str
    
    def _get_backend_url(self, configs: UserConfigs) -> str:
        backend_choice = configs.backend
        if backend_choice is None:
            backend_choice = storage_configs.default_backend
        
        url = storage_configs.backends[backend_choice]
        return url