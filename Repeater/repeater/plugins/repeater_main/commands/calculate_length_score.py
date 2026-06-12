from ..assist import PersonaInfo, SendMsg
from ..cmd_info import CmdTypes
from ..command_register import(
    CommandCaller,
    CommandPackage
)

@CommandCaller.register
class CalculateLengthScore(CommandPackage):
    cmd = "calculateLengthScore"
    aliases = {
        "cls",
        "CLS",
        "calculate_length_score",
        "Calculate_Length_Score",
        "CalculateLengthScore",
        "CALCULATE_LENGTH_SCORE",
    }
    cmd_type = CmdTypes.OTHER

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        text = persona_info.message_striped_str
        length = len(text)
        length_score = send_msg.text_length_score(text)
        length_score_threshold = send_msg.text_length_score_threshold
        await send_msg.send_prompt(
            f"Text Length: {length}\n"
            f"Length Score: {length_score}\n"
            f"Now Threshold: {length_score_threshold}\n"
        )