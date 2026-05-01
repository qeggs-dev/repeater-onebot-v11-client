from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CommandPackage
from ..._clients import ContextClient, PromptClient, ConfigClient


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

    @property
    def component(self) -> str:
        return f"Mixed.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)
        response_context = await context_client.delete()
        response_prompt = await prompt_client.delete()
        response_config = await config_client.delete()
        await send_msg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )