from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from ..._clients import ContextClient, PromptClient, ConfigClient

@CommandCaller.register
class SessionBranchBindFrom(CommandPackage):
    cmd = "sessionBranchBindFrom"
    aliases = {
        "sbbf",
        "SBBF",
        "session_branch_bind_from",
        "Session_Branch_Bind_From",
        "SessionBranchBindFrom",
        "SESSION_BRANCH_BIND_FROM",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)

        context_response = await context_client.bind_from(msg)
        prompt_response = await prompt_client.bind_from(msg)
        config_response = await config_client.bind_from(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )   