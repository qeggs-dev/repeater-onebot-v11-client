from ..._bases import DownloadFromNexus, UserdataCmdsType
from ....command_register import CommandCaller
from ....clients import ContextClient


@CommandCaller.register
class ContextDownloadFromNexus(DownloadFromNexus):
    cmd = "contextDownloadFromNexus"
    aliases = {
        "cdfn",
        "CDFN",
        "context_download_from_nexus",
        "Context_Download_From_Nexus",
        "ContextDownloadFromNexus",
        "CONTEXT_DOWNLOAD_FROM_NEXUS",
    }
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT