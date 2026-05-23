from ..assist import (
    get_first_mentioned_user,
    PersonaInfo,
    Namespace,
    SendMsg
)
from ..command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from ..command_register import CommandCaller, CommandPackage


@CommandCaller.register
class GetNamespace(CommandPackage):
    cmd = "getNamespace"
    aliases = {
        "gns",
        "GNS",
        "get_namespace",
        "Get_Namespace",
        "GetNamespace",
        "GET_NAMESPACE",
    }
    cmd_type = CmdTypes.NAMESPACE

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        mentioned_id = get_first_mentioned_user(persona_info._message_event)
        group_id = persona_info.group_id
        namespace = persona_info.namespace
        if mentioned_id is None:
            await send_msg.send_prompt(namespace.namespace_str)
        else:
            await send_msg.send_prompt(
                Namespace(
                    mode=namespace.mode,
                    group_id=group_id,
                    user_id=int(mentioned_id)
                ).namespace_str
            )