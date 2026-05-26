from __future__ import annotations
from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from typing import AsyncGenerator, Container
from ._assist_func import (
    handle_at_with_name,
    image_to_text
)
from ..client_net_configs import storage_configs
from ._namespace import MessageSource, Namespace
from ._image_downloader import ImageDownloader
from nonebot import logger
from datetime import datetime
from pydantic import ValidationError
from ._enter_type import EnterType

class PersonaInfo:
    def __init__(self, bot: Bot, event: MessageEvent, args: Message | None = None):
        self._bot: Bot = bot
        self._message_event: MessageEvent = event
        self._args: Message | None = args
        self._group_id: int | None = None
        self._source: MessageSource = MessageSource.GROUP
        self._source = MessageSource(event.message_type.strip().lower())
        self._enter_type: EnterType = EnterType.Command
        self._raw_message_event: MessageEvent | None = None
        self._self_id: int = int(bot.self_id)

        if self._source == MessageSource.GROUP:
            try:
                self._group_id = int(event.model_dump()["group_id"])
                if self._group_id is None:
                    raise ValueError("Is Group, But Group ID is None")
            except KeyError:
                raise ValueError("Is Group, But Group ID is Not Found")
        
        self._superusers: set[int] = set(int(user) for user in self._bot.config.superusers)
    
    @classmethod
    def from_command(cls, bot: Bot, event: MessageEvent, args: Message | None = None):
        persona_info = cls(
            bot = bot,
            event = event,
            args = args
        )
        persona_info._enter_type = EnterType.Command
        return persona_info
    
    @classmethod
    def from_message(cls, bot: Bot, event: MessageEvent):
        persona_info = cls(
            bot = bot,
            event = event
        )
        persona_info._enter_type = EnterType.Message
        return persona_info
    
    @classmethod
    def from_horizontal(cls, persona_info: PersonaInfo):
        persona_info = cls(
            bot = persona_info.bot,
            event = persona_info.event,
            args = persona_info.args
        )
        persona_info._enter_type = EnterType.Horizontal
        return persona_info
    
    async def from_reference_chain(self) -> AsyncGenerator[PersonaInfo, None]:
        async for event in self.get_reply_chain():
            persona_info = self.__class__(
                bot = self.bot,
                event = event
            )
            yield persona_info
    
    async def from_reference(self) -> PersonaInfo | None:
        event = await self.get_raw_message_event()
        reply_id: str | None = None
        for message in event.message:
            if message.type == "reply":
                reply_id = message.data["id"]
                break
        if reply_id is None:
            return None
        response = await self.bot.get_msg(message_id = reply_id)
        response["post_type"] = "message"
        reply_event = MessageEvent(**response)
        persona_info = self.__class__(
            bot = self.bot,
            event = reply_event
        )
        return persona_info
    
    def namespace_from_this_group(self, user_id: int):
        if self._source == MessageSource.GROUP:
            return Namespace(
                mode = MessageSource.GROUP,
                group_id = self._group_id,
                user_id = user_id
            )
        else:
            return Namespace(
                mode = MessageSource.PRIVATE,
                user_id = user_id
            )
    
    @property
    def enter_type(self) -> EnterType:
        return self._enter_type
    
    def __bool__(self) -> bool:
        for message in self.message:
            if message.type not in  ["at", "text", "reply"]:
                return True
            if message.type == "text":
                if message.data["text"]:
                    return True
        return False
    
    @property
    def is_superuser(self) -> bool:
        if self._bot.config.superusers is None:
            return False
        return self.user_id in self.superusers
    
    @property
    def is_self(self) -> bool:
        return self.user_id == self.self_id
    
    @property
    def self_id(self) -> int:
        return self._self_id
    
    @property
    def superusers(self) -> set[int]:
        return self._superusers.copy()
    
    @property
    def message_id(self) -> int:
        return self._message_event.message_id

    @property
    def group_id(self) -> int | None:
        if self._group_id is None:
            return None
        return self._group_id
    
    @property
    def user_id (self) -> int:
        return self._message_event.user_id
    
    @property
    def nickname(self) -> str | None:
        return self._message_event.sender.nickname
    
    @property
    def card(self) -> str | None:
        return self._message_event.sender.card
    
    @property
    def display_name(self) -> str:
        if self.card:
            return self.card
        else:
            if self.nickname is not None:
                return self.nickname
            return ""
    
    @property
    def age(self) -> int | None:
        return self._message_event.sender.age
    
    @property
    def gender(self) -> str | None:
        return self._message_event.sender.sex
    
    @property
    def bot(self):
        return self._bot
    
    @property
    def bots(self):
        return get_bots()
    
    @property
    def event(self):
        return self._message_event

    @property
    def namespace(self):
        if self._source == MessageSource.GROUP:
            return Namespace(
                mode = MessageSource.GROUP,
                group_id = self._group_id,
                user_id = self.user_id
            )
        else:
            return Namespace(
                mode = MessageSource.PRIVATE,
                user_id = self.user_id
            )
    
    @property
    def namespace_str(self):
        return self.namespace.namespace_str
    
    @property
    def public_namespace_str(self) -> str:
        return self.namespace.public_space_id
    
    @property
    def event_message(self) -> Message:
        return self._message_event.message
    
    @property
    def message(self) -> Message:
        if self._args is not None:
            return self._args.copy()
        else:
            return self._message_event.message.copy()
    
    @property
    def args(self) -> Message:
        if self._args is not None:
            return self._args.copy()
        else:
            return Message()
    
    @property
    def event_message_str(self) -> str:
        return self.event_message.extract_plain_text()
    
    @property
    def message_str(self) -> str:
        return self.message.extract_plain_text()
    
    @property
    def message_striped_str(self) -> str:
        return self.message_str.strip()
    
    @property
    def event_message_striped_str(self) -> str:
        return self.event_message_str.strip()
    
    @property
    def args_str(self) -> str:
        return self.args.extract_plain_text()
    
    @property
    def reply(self):
        return MessageSegment.reply(self.message_id)
    
    @property
    def source(self) -> MessageSource:
        return self._source
    
    @property
    def noself_at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                mentioned_id = segment.data["qq"]
                # 检查是否@的是非机器人用户
                if mentioned_id != self._bot.self_id:
                    at_list.append(mentioned_id)
        return at_list
    
    @property
    def at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                at_list.append(segment.data["qq"])
        return at_list
    
    async def handle_at_with_name(self):
        return await handle_at_with_name(self._bot, self._message_event)
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True, excluded_tags:Container[str] = {}) -> Message:
        """将图片转换为文字"""
        if "image" not in self.message:
            return self.message
        outmsg = Message()
        for segment in self.message:
            if segment.type == "image":
                ocrout = await self._bot.ocr_image(image = segment.data["url"])
                text = ""
                tag = segment.data.get("summary", "")
                for item in ocrout:
                    text += item["text"] + "\n"
                if text.endswith("\n"):
                    text = text[:-1]
                if tag not in excluded_tags:
                    text = f"[Image tag:{tag}]\n{text}"
                if text.strip():
                    text = format.format(text = text)
                    if cite:
                        text = text.replace("\n", "\n> ")
                    outmsg.append(MessageSegment(type = "text", data = {"text": text}))
                else:
                    outmsg.append(segment)
            else:
                outmsg.append(segment)
        return outmsg
    
    @property
    def plaintext_message(self) -> str:
        return self.message.extract_plain_text()
    
    async def get_images_url(self, base64: bool | None = None) -> list[str]:
        if base64 is None:
            base64 = storage_configs.use_base64_image_url
        images: list[str] = []
        if "image" in self.message:
            async with ImageDownloader(
                self.message,
                timeout=storage_configs.download_image_timeout
            ) as downloader:
                if base64:
                    get_image_url = downloader.download_image_to_base64()
                    async for image_url in get_image_url:
                        if image_url is not None:
                            images.append(image_url)
                else:
                    for image_url in downloader.get_images():
                        images.append(image_url)
        return images
    
    def get_video_url(self) -> list[str]:
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "video":
                urls.append(msg.data["url"])
        return urls
    
    def get_audio_url(self) -> list[str]:
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "record":
                urls.append(msg.data["url"])
        return urls
    
    async def get_reply_chain(self) -> AsyncGenerator[MessageEvent, None]:
        """
        获取回复链

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，那么它将会在该部分直接退出解析
        """
        event = await self.get_raw_message_event()
        message: Message = event.message
        times: int = 0
        try:
            while True:
                if times > storage_configs.max_reply_chain_length:
                    break
                reply_messages = await self.get_reply_msgs(message)
                if len(reply_messages) == 1:
                    event = reply_messages[0]
                    yield event
                    message = event.message
                else:
                    break
                times += 1
        finally:
            if times == 0:
                logger.warning(
                    "Reply chain is not found"
                )
    
    async def get_reply_msgs(self, message: Message | None = None) -> list[MessageEvent]:
        msgs: list[MessageEvent] = []
        if message is None:
            message = self._message_event.message
        for msg in message:
            if msg.type == "reply":
                reply_msg = await self._bot.get_msg(message_id=msg.data["id"])

                # 兼容 MessageEvent
                reply_msg["post_type"] = "message"
                msgs.append(
                    MessageEvent(**reply_msg)
                )
        if not msgs:
            logger.warning(
                "Reply is not found"
            )
        return msgs
    
    async def get_forward_msgs(self) -> list[MessageEvent]:
        msgs: list[MessageEvent] = []

        for msg in self._message_event.message:
            if msg.type == "forward":
                forward_msg = await self._bot.get_forward_msg(id=msg.data["id"])
                messages = forward_msg["messages"]
                for message in messages:
                    msgs.append(MessageEvent(**message))
        if not msgs:
            logger.warning(
                "Forward is not found"
            )
        return msgs
    
    @staticmethod
    def generates_text_from_messages_list(messages: list[dict | MessageEvent]):
        text_buffer: list[str] = []
        validation_failure_counter: int = 0
        for message in messages:
            try:
                if isinstance(message, MessageEvent):
                    event = message
                else:
                    event = MessageEvent(**message)
                nick_name = event.sender.card or event.sender.nickname
                text = event.message
                time = datetime.fromtimestamp(event.time)
            except ValidationError:
                try:
                    nick_name = message["sender"]["card"] or message["sender"]["nickname"]
                    text = message['message']
                    time = datetime.fromtimestamp(message["time"])
                except KeyError:
                    validation_failure_counter += 1
                    continue
            
            time_str = time.strftime("%Y-%m-%d %H:%M:%S")
            text_buffer.append(
                f"[{time_str}]{nick_name}: {text}"
            )

        if validation_failure_counter > 0:
            text_buffer.append(f"Validation Failure: {validation_failure_counter}")
        return "\n".join(text_buffer)
    
    async def get_raw_message_event(self) -> MessageEvent:
        response = await self.bot.get_msg(
            message_id = self.message_id
        )
        # 兼容 MessageEvent
        response["post_type"] = "message"
        return MessageEvent(**response)