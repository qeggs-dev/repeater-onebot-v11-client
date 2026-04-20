from ..._bases import DownloadFromNexus
from ....command_register import CommandCaller
from ..._clients import ContextClient


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

    def get_client(self, persona_info):
        return ContextClient(persona_info)