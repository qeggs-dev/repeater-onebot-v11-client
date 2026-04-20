import json
from .package import CommandPackage
from ..assist import PersonaInfo, SendMsg
from typing import Type, Callable, Awaitable
from nonebot import on_command, on_message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.exception import NoneBotException
from .listen_type import ListenType
from nonebot import logger

class CommandCaller:
    commands: list[CommandPackage] = []

    @staticmethod
    def get_message_handler(package: CommandPackage, matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent, Message], Awaitable[None]]:
        if package.empty_handler:
            async def command_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> None:
                pass
        else:
            async def command_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> None:
                logger.info(
                    "Run command handler: {name}",
                    name = package.component,
                )
                persona_info = PersonaInfo(bot, event, args)
                send_msg = SendMsg(package.component, matcher, persona_info)
                try:
                    await package.handler(persona_info, send_msg)
                except Exception as e:
                    await package.on_error(e, persona_info, send_msg)
        return command_handler
    
    def get_message_handler(package: CommandPackage, matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent], Awaitable[None]]:
        if package.empty_handler:
            async def message_handler(bot: Bot, event: MessageEvent):
                pass
        else:
            async def message_handler(bot: Bot, event: MessageEvent):
                logger.info(
                    "Run message handler: {name}",
                    name = package.component,
                )
                persona_info = PersonaInfo(bot, event)
                send_msg = SendMsg(package.component, matcher, persona_info)
                try:
                    if send_msg.is_debug_mode:
                        await package.on_debug_mode(persona_info, send_msg)
                    await package.handler(persona_info, send_msg)
                except Exception as e:
                    await package.on_error(e, persona_info, send_msg)
        return message_handler

    @classmethod
    def register(cls, package: Type[CommandPackage]) -> None:
        if package.enabled:
            package_instance = package()
            matcher = cls._get_matcher(package_instance)
                
            match package_instance.listen_type:
                case ListenType.Command:
                    logger.info(
                        "Register command: {name}\nCommand: {command}\nAliases:\n{aliases}",
                        name = package_instance.component,
                        command = package_instance.cmd,
                        aliases = json.dumps(list(package_instance.aliases), indent = 4, ensure_ascii = False),
                    )
                    handler = cls.get_message_handler(package_instance, matcher)
                case ListenType.Message:
                    logger.info(
                        "Register command: {name}",
                        name = package_instance.component
                    )
                    handler = cls.get_message_handler(package_instance, matcher)
                case _:
                    raise ValueError(f"{package_instance.listen_type} is not supported")
            
            matcher.append_handler(handler)
            cls.commands.append(package_instance)
        return package
    
    @staticmethod
    def _get_matcher(package: CommandPackage) -> Type[Matcher]:
        match package.listen_type:
            case ListenType.Command:
                matcher = on_command(
                    cmd = package.cmd,
                    rule = package.rule,
                    aliases = set(package.aliases),
                    force_whitespace = package.force_whitespace,
                    permission = package.permission,
                    handlers = package.handlers,
                    temp = package.temp,
                    expire_time = package.expire_time,
                    priority = package.priority,
                    block = package.block,
                    state = package.state,
                )
            case ListenType.Message:
                matcher = on_message(
                    rule = package.rule,
                    permission = package.permission,
                    handlers = package.handlers,
                    temp = package.temp,
                    expire_time = package.expire_time,
                    priority = package.priority,
                    block = package.block,
                    state = package.state,
                )
            case _:
                raise ValueError(f"Unknown listen type: {package.listen_type}")
        return matcher