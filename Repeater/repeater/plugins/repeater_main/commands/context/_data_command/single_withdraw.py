from ....assist import PersonaInfo, SendMsg
from ....command_register import CommandCaller, CommandPackage
from ..._clients import ContextClient


@CommandCaller.register
class SingleWithdraw(CommandPackage):
    cmd = "singleWithdraw"
    aliases = {
        "sw",
        "SW",
        "single_withdraw",
        "Single_Withdraw",
        "SingleWithdraw",
        "SINGLE_WITHDRAW",
    }

    @property
    def component(self) -> str:
        return f"Context.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        context_client = ContextClient(persona_info)
        if persona_info.args_str:
            try:
                num = int(persona_info.args_str)
            except ValueError:
                await send_msg.send_error("Please input a valid number")
                return

            if num < 1:
                await send_msg.send_error("Please input a number greater than 0")
                return
        else:
            num = 1

        response = await context_client.withdraw(num, paired=False)

        if response.code == 200:
            data = response.get_data()
            if data is None:
                await send_msg.send_error("Unable to process data.")
                return
            await send_msg.send_prompt(
                f"Deleted: {data.deleted}\n"
                f"Remaining: {len(data.context)}\n"
            )
        else:
            await send_msg.send_response_check_code(response, "Withdraw Failed")