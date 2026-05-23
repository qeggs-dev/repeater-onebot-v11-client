from ....assist import PersonaInfo, SendMsg
from ....command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from ..._clients import PromptClient

@CommandCaller.register
class SetPrompt(CommandPackage):
    cmd = "setPrompt"
    aliases = {
        "sp",
        "SP",
        "set_prompt",
        "Set_Prompt",
        "SetPrompt",
        "SET_PROMPT",
    }
    cmd_type = CmdTypes.PROMPT

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        msg = persona_info.message_striped_str

        prompt_client = PromptClient(persona_info)
        response = await prompt_client.set_prompt(msg)
        await send_msg.send_response_check_code(response, f"Set Prompt {'successfully' if response.code == 200 else 'failed'}")