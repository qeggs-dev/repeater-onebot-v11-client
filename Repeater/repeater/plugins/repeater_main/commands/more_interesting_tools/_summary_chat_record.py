import asyncio
from ...assist import PersonaInfo, SendMsg, MessageSource, CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ChatClient, ChatSendMsg


@CommandCaller.register
class SummaryChatRecord(CommandPackage):
    cmd = "summaryChatRecord"
    aliases = {
        "scr",
        "SCR",
        "summary_chat_record",
        "Summary_Chat_Record",
        "SummaryChatRecord",
        "SUMMARY_CHAT_RECORD",
    }
    cmd_type = CmdTypes.OTHER

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        if persona_info.source == MessageSource.PRIVATE:
            await send_msg.send_error("The current feature cannot be used in private chat.")

        group_id = persona_info.group_id

        try:
            n = int(persona_info.message_striped_str)
        except (ValueError, TypeError):
            await send_msg.send_error("Please enter a valid number.")

        if n > 0:
            message_list = await persona_info.cached_api.get_group_msg_history(
                group_id=group_id,
                count=n
            )

            text = await asyncio.to_thread(
                persona_info.generates_text_from_messages_list,
                message_list["messages"]
            )

            if text:
                text = f"{text}\n\n---\n\nPlease summarize the above chat record."

            chat_client = ChatClient(persona_info)
            response = await chat_client.send_message(
                add_metadata=False,
                message=text
            )
            chat_sendmsg = ChatSendMsg(
                send_msg.component,
                persona_info,
                send_msg.matcher,
                response
            )
            await chat_sendmsg.send()
        else:
            await send_msg.send_error("The input must be a positive integer!")