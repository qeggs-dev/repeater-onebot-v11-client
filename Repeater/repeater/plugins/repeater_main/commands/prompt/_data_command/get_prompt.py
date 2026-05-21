from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from ..._clients import PromptClient

@CommandCaller.register
class GetPrompt(CommandPackage):
    cmd = "getPrompt"
    aliases = {
        "gp",
        "GP",
        "get_prompt",
        "Get_Prompt",
        "GetPrompt",
        "GET_PROMPT",
    }
    cmd_type = CmdType.PROMPT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        prompt_client = PromptClient(persona_info)
        response = await prompt_client.get_prompt()
        if response:
            if response.text:
                await send_msg.send_render_prompt(response.text)
            else:
                await send_msg.send_prompt("[No Prompt]")
        else:
            await send_msg.send_response(response)