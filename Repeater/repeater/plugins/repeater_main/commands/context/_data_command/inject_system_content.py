from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient, ContentRole, ContentUnit


@CommandCaller.register
class InjectSystemContent(CommandPackage):
    cmd = "injectSystemContent"
    aliases = {
        "isc",
        "ISC",
        "inject_system_content",
        "Inject_System_Content",
        "InjectSystemContent",
        "INJECT_SYSTEM_CONTENT",
    }
    type = CmdType.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        response = await context_client.inject_context(
            content_unit=ContentUnit(
                content=persona_info.message_striped_str,
                role=ContentRole.SYSTEM
            )
        )

        if response:
            await send_msg.send_response(
                response,
                message="Inject System Content Successful"
            )
        else:
            await send_msg.send_response(
                response,
                message="Inject System Content Failed"
            )