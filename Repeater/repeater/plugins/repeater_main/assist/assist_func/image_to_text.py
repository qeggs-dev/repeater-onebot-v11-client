from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters import Bot
from typing import Container

async def image_to_text(
        bot:Bot,
        message: Message,
        format: str = "{text}",
        cite: bool = True,
        ensure_empty_when_text_exists: bool = False,
        excluded_tags: Container[str] | None = None,
    ) -> Message:
    """
    将图片转换为文字

    :param bot: 机器人实例
    :param message: 消息对象
    :param format: 转换后的格式，需要填写 {text} 占位符
    :param cite: 是否引用原始消息
    :param ensure_empty_when_text_exists: 如果没有识别出文字，且消息中有文本内容，是否返回以空识别结果输出
    """
    if "image" not in message:
        return message
    outmsg = Message()
    for segment in message:
        if segment.type == "image":
            ocrout = await bot.ocr_image(image = segment.data["url"])
            text = ""
            summary = segment.data.get("summary", "")
            for item in ocrout:
                text += item["text"] + "\n"
            if text.endswith("\n"):
                text = text[:-1]
            text = format.format(text = text)
            if (ensure_empty_when_text_exists and message.extract_plain_text().strip()) or text.strip():
                if excluded_tags is not None and summary in excluded_tags:
                    text = f"[Image tag:{summary}]\n{text}"
                if cite:
                    text = text.replace("\n", "\n> ")
                outmsg.append(MessageSegment(type = "text", data = {"text": text}))
            else:
                outmsg.append(segment)
        else:
            outmsg.append(segment)
    return outmsg