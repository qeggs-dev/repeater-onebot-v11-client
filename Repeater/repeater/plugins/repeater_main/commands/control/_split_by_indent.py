from typing import Iterable, Generator
from nonebot.adapters.onebot.v11 import Message, MessageSegment

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
            now_message.clear()
            results.append(line)
        elif indent >= last_indent:
            now_message.extend(line)
        elif indent < last_indent:
            results.append(now_message)
            now_message.clear()
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
    results: list[Message] = []
    now_message = Message()
    
    for segment in message:
        segments = segment_splitlines(segment)
        if len(segments) > 1:
            for segment in segments:
                now_message.append(segment)
                results.append(now_message)
                now_message = Message()
        else:
            now_message.append(segment)
    
    if now_message:
        results.append(now_message)
    
    return results

def segment_splitlines(
    segment: MessageSegment,
) -> list[MessageSegment]:
    if segment.type != "text":
        return [segment]
    else:
        text: str = segment.data["text"]
        if not isinstance(text, str):
            raise ValueError("text must be str")
        
        if "\n" in text:
            return [MessageSegment.text(t) for t in text.split("\n")]
        else:
            return [segment]