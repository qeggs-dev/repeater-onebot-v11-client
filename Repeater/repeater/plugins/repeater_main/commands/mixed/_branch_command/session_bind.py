from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class SessionBranchBind(CommandPackage):
    cmd = "sessionBranchBind"
    aliases = {
        "sbb",
        "SBB",
        "session_branch_bind",
        "Session_Branch_Bind",
        "SessionBranchBind",
        "SESSION_BRANCH_BIND",
    }
    cmd_type = CmdType.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)

        context_response = await context_client.bind(msg)
        prompt_response = await prompt_client.bind(msg)
        config_response = await config_client.bind(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )
