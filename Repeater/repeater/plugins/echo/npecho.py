from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)

no_promot_echo = on_command("noPromptEcho", aliases={"npecho", "NPECHO", "no_prompt_echo", "No_Prompt_Echo", "NoPromptEcho"}, rule=to_me(), block=True)

@no_promot_echo.handle()
async def np_echo_handle(matcher: Matcher, args: Message = CommandArg()):
    if args:
        matcher.set_arg("echo_text", args)

@no_promot_echo.receive("echo_text")
async def np_echo_got_text(args: Message = Arg("echo_text")):
    if isinstance(args, Message):
        # 如果是消息对象，则直接返回
        await no_promot_echo.finish(args)
    else:
        # 回退到纯文本模式
        await no_promot_echo.finish(ArgPlainText())