from urllib.parse import urljoin
from ...client_net_configs import *
from ...assist import BaseClient
from ...logger import logger

class UserFileClient(BaseClient):
    # region get_utl
    async def get_user_data_file_url(self):
        logger.info("Get user data file url", module = "user_file.core")
        return urljoin(base_url, f"{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self._persona_info.namespace_str}.zip")
    # endregion

    # region package_user_space_url
    async def package_user_space_url(self):
        logger.info("Package user space url", module = "user_file.core")
        return urljoin(base_url, f"{PACKAGE_USER_SPACE_ROUTE}/{self._persona_info.namespace_str}.zip")