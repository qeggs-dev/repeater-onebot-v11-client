import re
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg, ContentRole
from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class GenerateCandidateAnswer(BaseChat):
    cmd = "generateCandidateAnswer"
    aliases = {
        "gca",
        "GCA",
        "generate_candidate_answer",
        "Generate_Candidate_Answer",
        "GenerateCandidateAnswer",
        "GENERATE_CANDIDATE_ANSWER"
    }
    documents = f"""
        Initiate a text generation request in the opposite role,
        let AI mimic user-generated content.
        Warning: the presence of Tool Calls may cause an error in your application.
        
        Usage:
        ```
        /{cmd}
        ```
    """
    no_input = True

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

    @staticmethod
    def filters(message: str) -> str:
        return ChatClient.metadata_pattern.sub("", message)