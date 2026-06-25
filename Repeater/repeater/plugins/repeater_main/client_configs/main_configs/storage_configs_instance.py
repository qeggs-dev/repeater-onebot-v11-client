from ...config_loader import Loader, Mode
from .storage_configs_class import StorageConfigs

loader: Loader[StorageConfigs] = Loader(
    model=StorageConfigs,
    path="configs/main_api.json",
    mode=Mode.JSON
)
storage_configs: StorageConfigs = loader.load(unexist_create = True)