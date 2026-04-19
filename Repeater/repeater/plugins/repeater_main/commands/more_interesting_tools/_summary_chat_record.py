import asyncio
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import CommandArg

from ...assist import PersonaInfo, SendMsg, MessageSource
from .._clients import ChatClient, ChatSendMsg

summary_chat_record = on_command("summaryChatRecord", aliases={"scr", "summary_chat_record", "Summary_Chat_Record", "SummaryChatRecord"}, rule=to_me(), block=True)

@summary_chat_record.handle()
async def handle_summary_chat_record(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("More.Summary_Chat_Record", summary_chat_record, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    
    if persona_info.source == MessageSource.PRIVATE:
        await send_msg.send_error("The current feature cannot be used in private chat.")
    
    group_id = persona_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await send_msg.send_error("Please enter a valid number.")
    if n > 0:
        message_list = await bot.get_group_msg_history(
            group_id = group_id,
            count = n
        )

        text = await asyncio.to_thread(persona_info.generates_text_from_messages_list, message_list["messages"])

        if text:
            text = f"{text}\n\n---\n\nPlease summarize the above chat record."

        chat_client = ChatClient(persona_info)
        response = await chat_client.send_message(
            add_metadata = False,
            message = text
        )
        chat_sendmsg = ChatSendMsg(
            send_msg.component,
            persona_info,
            summary_chat_record,
            response
        )
        await chat_sendmsg.send()
        
    else:
        await send_msg.send_error("The input must be a positive integer!")