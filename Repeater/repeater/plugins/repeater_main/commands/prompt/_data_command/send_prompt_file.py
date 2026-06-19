from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import PromptClient


@CommandCaller.register
class SendPromptFile(CommandPackage):
    cmd = "sendPromptFile"
    aliases = {
        "spf",
        "SPF",
        "send_prompt_file",
        "Send_Prompt_File",
        "SendPromptFile",
        "SEND_PROMPT_FILE",
    }
    cmd_type = CmdTypes.PROMPT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        
        user_configs = await persona_info.get_user_configs()
        prompt_client = PromptClient(persona_info, user_configs)
        file_url = prompt_client.get_prompt_url()
        await send_msg.send_file(file_url, f"{persona_info.namespace_str}_User_Prompt.md")