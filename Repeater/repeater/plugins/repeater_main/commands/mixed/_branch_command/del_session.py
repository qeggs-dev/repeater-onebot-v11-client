from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class DeleteSession(CommandPackage):
    cmd = "delSession"
    aliases = {
        "ds",
        "DS",
        "delete_session",
        "Delete_Session",
        "DeleteSession",
        "DELETE_SESSION",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        user_configs = await persona_info.get_user_configs()
        context_client = ContextClient(persona_info, user_configs)
        prompt_client = PromptClient(persona_info, user_configs)
        config_client = ConfigClient(persona_info, user_configs)
        response_context = await context_client.delete()
        response_prompt = await prompt_client.delete()
        response_config = await config_client.delete()
        await send_msg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )