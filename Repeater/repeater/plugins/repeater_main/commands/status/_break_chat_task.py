from ...assist import PersonaInfo, SendMsg, CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ChatClient

@CommandCaller.register
class BreakChatTask(CommandPackage):
    cmd = "breakChatTask"
    aliases = {
        "bct",
        "BCT",
        "break_chat_task",
        "Break_Chat_Task",
        "BreakChatTask",
        "BREAK_CHAT_TASK",
    }
    cmd_type = CmdTypes.STATUS

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        core = ChatClient(persona_info)
        response = await core.break_chat_task()
        if response.code == 200:
            break_response = response.get_data()
            if break_response is None:
                await send_msg.send_error("Failed parsing response data.")
            else:
                await send_msg.send_prompt(break_response.msg)
        else:
            await send_msg.send_error_response(response)