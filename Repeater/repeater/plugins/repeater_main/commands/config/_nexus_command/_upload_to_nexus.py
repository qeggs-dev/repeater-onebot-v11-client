from ..._bases import UploadToNexus
from ....command_register import CommandCaller
from ....clients import ConfigClient


@CommandCaller.register
class ConfigUploadToNexus(UploadToNexus):
    cmd = "configUploadToNexus"
    aliases = {
        "cfgutn",
        "CFGUTN",
        "config_upload_to_nexus",
        "Config_Upload_To_Nexus",
        "ConfigUploadToNexus",
        "CONFIG_UPLOAD_TO_NEXUS",
    }

    def get_client(self, persona_info):
        return ConfigClient(persona_info)