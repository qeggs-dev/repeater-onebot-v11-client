from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from ..._clients import ContextClient
from ....assist import PersonaInfo, SendMsg

single_withdraw = on_command("singleWithdraw", aliases={"sw", "single_withdraw", "Single_Withdraw", "SingleWithdraw"}, rule=to_me(), block=True)

@single_withdraw.handle()
async def handle_single_withdraw(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Context.Single_Withdraw", single_withdraw, persona_info)

    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()

    context_client = ContextClient(persona_info)
    if persona_info.args_str:
        try:
            num = int(persona_info.args_str)
        except ValueError:
            await send_msg.send_error("Please input a valid number")
        
        if num < 1:
            await send_msg.send_error("Please input a number greater than 0")
    else:
        num = 1

    response = await context_client.withdraw(num, paired = False)

    if response.code == 200:
        data = response.get_data()
        if data is None:
            await send_msg.send_error("Unable to process data.")
        await send_msg.send_prompt(
            f"Deleted: {data.deleted}\n"
            f"Remaining: {len(data.context)}\n"
        )
        
    else:
        await send_msg.send_response_check_code(response, "Withdraw Failed")
