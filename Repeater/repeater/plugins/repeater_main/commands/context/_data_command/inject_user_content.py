from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import ContextClient, ContentRole, ContentUnit

@CommandCaller.register
class InjectUserContent(CommandPackage):
    cmd = "injectUserContent"
    aliases = {
        "iuc",
        "IUC",
        "inject_user_content",
        "Inject_User_Content",
        "InjectUserContent",
        "INJECT_USER_CONTENT",
    }
    cmd_type = CmdType.CONTEXT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        response = await context_client.inject_context(
            content_unit=ContentUnit(
                content=persona_info.message_striped_str,
                role=ContentRole.USER
            )
        )

        if response:
            await send_msg.send_response(
                response,
                message="Inject User Content Successful"
            )
        else:
            await send_msg.send_response(
                response,
                message="Inject User Content Failed"
            )