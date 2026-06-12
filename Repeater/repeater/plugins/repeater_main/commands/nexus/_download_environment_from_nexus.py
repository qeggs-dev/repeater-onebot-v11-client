from .._bases.base_nexus import DownloadFromNexus
from ...command_register import CommandCaller
from ...clients import NexusClient


@CommandCaller.register
class EnvironmentDownloadFromNexus(DownloadFromNexus):
    cmd = "envDownloadFromNexus"
    aliases = {
        "edfn",
        "EDFN",
        "env_download_from_nexus",
        "Env_Download_From_Nexus",
        "EnvDownloadFromNexus",
        "ENV_DOWNLOAD_FROM_NEXUS",
    }

    def get_client(self, persona_info):
        return NexusClient(persona_info)