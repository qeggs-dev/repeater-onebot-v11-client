from ..._bases import UploadToNexus
from ....command_register import CommandCaller
from ....clients import PromptClient


@CommandCaller.register
class PromptUploadToNexus(UploadToNexus):
    cmd = "promptUploadToNexus"
    aliases = {
        "putn",
        "PUTN",
        "prompt_upload_to_nexus",
        "Prompt_Upload_To_Nexus",
        "PromptUploadToNexus",
        "PROMPT_UPLOAD_TO_NEXUS",
    }

    def get_client(self, persona_info):
        return PromptClient(persona_info)