from ..._bases import UploadToNexus, UserdataCmdsType
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
    userdata_cmds_type: UserdataCmdsType = UserdataCmdsType.CONTEXT