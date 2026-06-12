from urllib.parse import urljoin
from ...client_net_configs import *
from ...assist import PersonaInfo
from ...logger import logger

class UserFileClient:
    def __init__(self, info: PersonaInfo):
        self._info = info
    
    # region get_utl
    async def get_user_data_file_url(self):
        logger.info("Get user data file url", module = "user_file.core")
        return urljoin(BASE_URL, f"{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self._info.namespace_str}.zip")
    # endregion

    # region package_user_space_url
    async def package_user_space_url(self):
        logger.info("Package user space url", module = "user_file.core")
        return urljoin(BASE_URL, f"{PACKAGE_USER_SPACE_ROUTE}/{self._info.namespace_str}.zip")