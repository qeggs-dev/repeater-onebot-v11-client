from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient, PromptClient, ConfigClient

@CommandCaller.register
class ChangeSession(CommandPackage):
    cmd = "changeSession"
    aliases = {
        "cs",
        "CS",
        "change_session",
        "Change_Session",
        "ChangeSession",
        "CHANGE_SESSION",
    }
    cmd_type = CmdType.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)
        response_context = await context_client.change_branch(persona_info.message_striped_str)
        response_prompt = await prompt_client.change_branch(persona_info.message_striped_str)
        response_config = await config_client.change_branch(persona_info.message_striped_str)
        await send_msg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )