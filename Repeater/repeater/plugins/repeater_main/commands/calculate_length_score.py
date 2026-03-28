from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ..assist import PersonaInfo, SendMsg

calculate_length_score = on_command("calculateLengthScore", aliases={"cls", "calculate_length_score", "Calculate_Length_Score", "CalculateLengthScore"}, rule=to_me(), block=True)

@calculate_length_score.handle()
async def handle_calculate_length_score(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    send_msg = SendMsg("Length_Score.Calculate", calculate_length_score, persona_info)
    text = persona_info.message_striped_str
    length = len(text)
    length_score = send_msg.text_length_score(text)
    length_score_threshold = send_msg.text_length_score_threshold
    await send_msg.send_prompt(
        f"Text Length: {length}\n"
        f"Length Score: {length_score}\n"
        f"Now Threshold: {length_score_threshold}\n"
    )