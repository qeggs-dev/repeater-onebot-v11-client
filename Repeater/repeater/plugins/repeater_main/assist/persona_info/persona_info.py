from __future__ import annotations

import aiofiles

from nonebot import get_bots
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from typing import AsyncGenerator, Container
from ..assist_func import (
    at_with_name,
    image_to_text,
    get_images_url,
    get_reply_msgs,
    get_forward_msgs,
    get_message_event,
    generates_text_from_messages_list,
    get_reply_chain
)
from ...client_net_configs import storage_configs
from ..namespace import MessageSource, Namespace
from ..network.image_downloader import ImageDownloader
from nonebot import logger
from datetime import datetime
from pydantic import ValidationError
from .enter_type import EnterType
from .file_info import FileInfo

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
    def from_command(cls, bot: Bot, event: MessageEvent, args: Message | None = None) -> PersonaInfo:
        persona_info = cls(
            bot = bot,
            event = event,
            args = args
        )
        persona_info._enter_type = EnterType.Command
        return persona_info
    
    @classmethod
    def from_message(cls, bot: Bot, event: MessageEvent) -> PersonaInfo:
        persona_info = cls(
            bot = bot,
            event = event
        )
        persona_info._enter_type = EnterType.Message
        return persona_info
    
    @classmethod
    def from_horizontal(cls, persona_info: PersonaInfo) -> PersonaInfo:
        persona_info = cls(
            bot = persona_info.bot,
            event = persona_info.event,
            args = persona_info.args
        )
        persona_info._enter_type = EnterType.Horizontal
        return persona_info
    
    async def from_raw_message_event(self, event: MessageEvent) -> PersonaInfo:
        event = self.get_message_event()
        cls = type(self)
        instance = cls(
            bot = self.bot,
            event = event,
            args = self.args,
        )
        instance._enter_type = self._enter_type
        return instance
    
    async def from_reference_chain(self) -> AsyncGenerator[PersonaInfo, None]:
        async for event in self.get_reply_chain():
            persona_info = self.__class__(
                bot = self.bot,
                event = event
            )
            yield persona_info
    
    async def from_reference(self) -> PersonaInfo | None:
        event = await self.get_message_event()
        reply_id: str | None = None
        for message in event.message:
            if message.type == "reply":
                reply_id = message.data["id"]
                break
        if reply_id is None:
            return None
        reply_event = await self.get_message_event(message_id = reply_id)
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
        return await at_with_name(self._bot, self._message_event)
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True, excluded_tags:Container[str] = {}) -> Message:
        """将图片转换为文字"""
        await image_to_text(
            self._bot,
            self.message,
            format = format,
            cite = cite,
            excluded_tags = excluded_tags
        )
    
    @property
    def plaintext_message(self) -> str:
        return self.message.extract_plain_text()
    
    async def get_images_url(self, base64: bool | None = None) -> list[str]:
        return await get_images_url(
            self.message,
            base64 = base64
        )
    
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
    
    def get_file_ids(self) -> list[str]:
        ids: list[str] = []
        for msg in self.message:
            if msg.type == "file":
                ids.append(msg.data["file_id"])
        return ids
    
    def get_file_urls(self) -> list[str]:
        urls: list[str] = []
        for msg in self.message:
            if msg.type == "file":
                urls.append(msg.data["url"])
        return urls
    
    async def get_file_info(self, file_id: str) -> FileInfo:
        response = await self.bot.get_file(file = file_id)
        return FileInfo(**response)
    
    async def get_file_name(self, file_id: str) -> str:
        file_info = await self.get_file_info(file_id)
        return file_info.file_name
    
    async def get_file_size(self, file_id: str) -> int:
        file_info = await self.get_file_info(file_id)
        return int(file_info.file_size)
    
    async def open_file(self, file_info: FileInfo) -> bytes:
        async with aiofiles.open(file_info.file, "rb") as f:
            return await f.read()
    
    async def open_text_file(self, file_info: FileInfo, encoding: str = "utf-8") -> str:
        async with aiofiles.open(file_info.file, "r", encoding = encoding) as f:
            return await f.read()
    
    async def get_reply_chain(self) -> AsyncGenerator[MessageEvent, None]:
        """
        获取回复链

        注：解析时，它会默认消息段中只有一个 reply 消息段，
        如果有存在多个，那么它将会在该部分直接退出解析
        """

        # 经过框架处理的 Event 中可能并未包含 reply 消息段
        # 需要重新获取原始 Event
        event = await self.get_message_event()
        message: Message = event.message

        return await get_reply_chain(
            self._bot,
            message
        )
    
    async def get_reply_msgs(self, message: Message | None = None) -> list[MessageEvent]:
        return await get_reply_msgs(
            self._bot,
            message if message is not None else self.message
        )
    
    async def get_forward_msgs(self) -> list[MessageEvent]:
        return await get_forward_msgs(
            self._bot,
            self.message
        )
    
    @staticmethod
    def generates_text_from_messages_list(messages: list[dict | MessageEvent]):
        return generates_text_from_messages_list(messages)
    
    async def get_message_event(self, message_id: int | None = None) -> MessageEvent:
        return get_message_event(
            self._bot,
            message_id if message_id is not None else self.message_id
        )