from ..._bases import DownloadFromNexus, UserdataCmdsType
from ....command_register import CommandCaller
from ....clients import PromptClient


@CommandCaller.register
class PromptDownloadFromNexus(DownloadFromNexus):
    cmd = "promptDownloadFromNexus"
    aliases = {
        "pdfn",
        "PDFN",
        "prompt_download_from_nexus",
        "Prompt_Download_From_Nexus",
        "PromptDownloadFromNexus",
        "PROMPT_DOWNLOAD_FROM_NEXUS",
    }
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.PROMPT