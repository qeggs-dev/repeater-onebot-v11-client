from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class SessionBranchCloneFrom(CommandPackage):
    cmd = "sessionBranchCloneFrom"
    aliases = {
        "sbcf",
        "SBCF",
        "session_branch_clone_from",
        "Session_Branch_Clone_From",
        "SessionBranchCloneFrom",
        "SESSION_BRANCH_CLONE_FROM",
    }
    type = CmdType.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)

        context_response = await context_client.clone_from(msg)
        prompt_response = await prompt_client.clone_from(msg)
        config_response = await config_client.clone_from(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )