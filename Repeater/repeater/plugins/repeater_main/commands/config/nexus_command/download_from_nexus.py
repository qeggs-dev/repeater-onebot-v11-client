from ..._bases import DownloadFromNexus, UserdataCmdsType
from ....command_register import CommandCaller

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
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONFIG