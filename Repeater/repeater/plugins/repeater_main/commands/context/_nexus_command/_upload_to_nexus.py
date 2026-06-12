from ..._bases import UploadToNexus
from ....command_register import CommandCaller
from ....clients import ContextClient


@CommandCaller.register
class ContextUploadToNexus(UploadToNexus):
    cmd = "contextUploadToNexus"
    aliases = {
        "cutn",
        "CUTN",
        "context_upload_to_nexus",
        "Context_Upload_To_Nexus",
        "ContextUploadToNexus",
        "CONTEXT_UPLOAD_TO_NEXUS",
    }

    def get_client(self, persona_info):
        return ContextClient(persona_info)