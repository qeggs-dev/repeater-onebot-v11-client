import re
from ...logger import logger

from .._clients import ChatClient, ChatSendMsg, ContentRole
from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller, CommandPackage

@CommandCaller.register
class GenerateCandidateAnswer(CommandPackage):
    cmd = "generateCandidateAnswer"
    aliases = {
        "gca",
        "generate_candidate_answer",
        "Generate_Candidate_Answer",
        "GenerateCandidateAnswer"
    }
    component = "Chat.Generate_Candidate_Answer"

    metadata_pattern = re.compile(r"> Message\s*?Metadata:.*?---(?:\r?\n)+", re.DOTALL | re.IGNORECASE)

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        message_text = persona_info.message_striped_str

        logger.info(
            "Received a message {message} from {namespace}",
            message = message_text,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )
        
        reply_msgs = await persona_info.get_reply_chain()
        if reply_msgs:
            reply_msgs_text = persona_info.generates_text_from_messages_list(reply_msgs)
            reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")

        core = ChatClient(persona_info)

        images: list[str] = await persona_info.get_images_url()

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
            },
            image_url = images
        )

        def filters(message: str) -> str:
            return self.metadata_pattern.sub("", message)

        send_msg = ChatSendMsg(
            send_msg.component,
            persona_info,
            send_msg.matcher,
            response,
            content_handler = filters
        )
        await send_msg.send()