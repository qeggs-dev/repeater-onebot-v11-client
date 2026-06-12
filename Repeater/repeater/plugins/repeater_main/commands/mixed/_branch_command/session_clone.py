from ....assist import PersonaInfo, SendMsg
from ....cmd_info import CmdTypes
from ....command_register import(
    CommandCaller,
    CommandPackage
)
from ....clients import ContextClient, PromptClient, ConfigClient


@CommandCaller.register
class SessionBranchClone(CommandPackage):
    cmd = "sessionBranchClone"
    aliases = {
        "sbc",
        "SBC",
        "session_branch_clone",
        "Session_Branch_Clone",
        "SessionBranchClone",
        "SESSION_BRANCH_CLONE",
    }
    cmd_type = CmdTypes.BRANCH_MIXED

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str

        context_client = ContextClient(persona_info)
        prompt_client = PromptClient(persona_info)
        config_client = ConfigClient(persona_info)

        context_response = await context_client.clone(msg)
        prompt_response = await prompt_client.clone(msg)
        config_response = await config_client.clone(msg)

        await send_msg.send_multiple_responses(
            (context_response, "Context"),
            (prompt_response, "Prompt"),
            (config_response, "Config"),
        )