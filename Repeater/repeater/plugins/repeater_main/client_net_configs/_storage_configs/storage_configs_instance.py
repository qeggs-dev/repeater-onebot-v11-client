from ...config_loader import Loader, Mode
from .storage_configs import StorageConfigs

loader: Loader[StorageConfigs] = Loader(
    model=StorageConfigs,
    path="configs/main_api.json",
    mode=Mode.JSON
)
storage_configs: StorageConfigs = loader.load(write_on_failure=True)