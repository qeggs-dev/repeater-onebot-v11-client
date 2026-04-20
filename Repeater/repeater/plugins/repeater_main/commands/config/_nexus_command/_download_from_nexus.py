from ..._bases import DownloadFromNexus
from ....command_register import CommandCaller
from ..._clients import ConfigClient

@CommandCaller.register
class ConfigDownloadFromNexus(DownloadFromNexus):
    cmd = "configDownloadFromNexus"
    aliases = {
        "cfgdfn",
        "CFGDFN",
        "config_download_from_nexus",
        "Config_Download_From_Nexus",
        "ConfigDownloadFromNexus",
        "CONFIG_DOWNLOAD_FROM_NEXUS"
    }

    def get_client(self, persona_info):
        return ConfigClient(persona_info)