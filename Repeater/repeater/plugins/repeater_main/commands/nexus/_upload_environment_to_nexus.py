from .._bases.base_nexus import UploadToNexus
from ...command_register import CommandCaller
from ...clients import NexusClient


@CommandCaller.register
class EnvironmentUploadToNexus(UploadToNexus):
    cmd = "envUploadToNexus"
    aliases = {
        "eutn",
        "EUTN",
        "env_upload_to_nexus",
        "Env_Upload_To_Nexus",
        "EnvUploadToNexus",
        "ENV_UPLOAD_TO_NEXUS",
    }

    def get_client(self, persona_info):
        return NexusClient(persona_info)