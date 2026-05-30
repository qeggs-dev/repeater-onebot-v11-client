from ...assist import PersonaInfo, SendMsg, MessageSource
from ...command_register import CommandCaller, ListenType
from .._bases import BaseChat

@CommandCaller.register
class SmartAt(BaseChat):
    listen_type: ListenType = ListenType.Message
    priority = 100
    documents = """
        Determines whether the input is null,
        to perform a build task,
        or output the specified text

        Usage:
        ```
        @Bot message
        ```

        Or:
        ```
        @Bot
        ```
    """

    async def empty_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> None: 
        if not persona_info:
            if persona_info.source == MessageSource.GROUP:
                await send_msg.send_hello()
            else:
                send_msg.break_handler()