from typing import Iterable, Generator
from nonebot.adapters.onebot.v11 import Message

def split_by_indent(
    message: Message,
    indent: int = 2,
    indent_char: str = " "
) -> list[Message]:
    results: list[Message] = []
    lines = splitlines(message)
    last_indent: int = 0
    now_message: Message = Message()
    for now_indent, line in enumerate_indent(lines, indent, indent_char):
        if now_indent == 0:
            now_message = Message() # 不能使用 clear，这会导致已经添加的 segment 被清空
            results.append(line)
        elif indent >= last_indent:
            now_message.extend(line)
        elif indent < last_indent:
            results.append(now_message)
            now_message = Message()
            now_message.extend(line)
        last_indent = now_indent
    
    if now_message:
        results.append(now_message)
    
    return results

def enumerate_indent(
    messages: Iterable[Message],
    indent: int = 2,
    indent_char: str = " ",
) -> Generator[tuple[int, Message], None, None]:
    if indent <= 0:
        raise ValueError("indent must be greater than 0")
    
    for message in messages:
        if not message:
            continue

        first_segment = message[0]
        if first_segment.type == "text":
            text = first_segment.data["text"]
            if not isinstance(text, str):
                raise TypeError("text segment must be str")
            
            indent_count: int = 0
            for char in text:
                if char == indent_char:
                    indent_count += 1
                else:
                    break
            
            yield indent_count // indent, message
        else:
            yield 0, message

def splitlines(
    message: Message
) -> list[Message]:
    cq_code_str = str(message)
    cq_codes = cq_code_str.splitlines()
    return [Message(cq_code) for cq_code in cq_codes if cq_code]
