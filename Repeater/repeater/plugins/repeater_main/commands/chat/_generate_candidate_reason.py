import re
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg, ContentRole
from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class GenerateCandidateReason(BaseChat):
    cmd = "generateCandidateReason"
    aliases = {
        "gcr",
        "GCR",
        "generate_candidate_reason",
        "Generate_Candidate_Reason",
        "GenerateCandidateReason",
        "GENERATE_CANDIDATE_REASON"
    }
    documents = f"""
        Initiate a text generation request in the opposite role and enable inference mode,
        let AI simulate user-generated content.
        Warning: the presence of a tool call may cause an application error.
        
        Usage:
        ```
        /{cmd}
        ```
    """
    no_input = True

    metadata_pattern = re.compile(r"> Message\s*?Metadata:.*?---(?:\r?\n)+", re.DOTALL | re.IGNORECASE)

    async def send_message(self, persona_info: PersonaInfo, send_msg: SendMsg):
        core = ChatClient(persona_info)

        response = await core.send_message(
            message = None,
            add_metadata = False,
            save_context = False,
            temporary_prompt = (
                "{%- if user_profile -%}\n"
                "{{user_profile}}\n"
                "{%- endif %}"
            ),
            history_msg_role_map = {
                ContentRole.USER: ContentRole.ASSISTANT,
                ContentRole.ASSISTANT: ContentRole.USER,
                ContentRole.SYSTEM: None,
                ContentRole.TOOLS: None
            }
        )

    @classmethod
    def filters(cls, message: str) -> str:
        return cls.metadata_pattern.sub("", message)