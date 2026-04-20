from ..._bases import DownloadFromNexus
from ....command_register import CommandCaller
from ..._clients import PromptClient


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

    def get_client(self, persona_info):
        return PromptClient(persona_info)