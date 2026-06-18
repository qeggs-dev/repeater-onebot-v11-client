from ..namespace import Namespace
from ...config_loader import AsyncLoader
from .config_object import UserConfigs

class UserConfigLoader:
    def __init__(self, namespace: Namespace):
        self.namespace = namespace
        self.loader: AsyncLoader[UserConfigs] = AsyncLoader(
            model = UserConfigs,
            path = f"user_configs/{namespace.namespace_str}.json"
        )
    
    async def load(self):
        try:
            configs = await self.loader.load()
        except Exception as e:
            configs = UserConfigs()
        return configs
    
    async def save(self, configs: UserConfigs):
        await self.loader.save(configs)