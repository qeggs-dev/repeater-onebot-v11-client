import sys
import json
import asyncio
from .package import CommandPackage
from ..assist import PersonaInfo, SendMsg, CmdTypes
from ..client_net_configs import storage_configs
from ..exceptions import *
from nonebot.exception import NoneBotException
from typing import Iterator, Type, Callable, Awaitable, TypeVar
from nonebot import on_command, on_message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from .listen_type import ListenType
from nonebot import logger
from .running_package import RunningPackage

T_Handler_Result = TypeVar("T_Handler_Result")

class CommandCaller:
    commands: dict[Type[CommandPackage[T_Handler_Result]], CommandPackage[T_Handler_Result]] = {}
    matchers: dict[Type[CommandPackage[T_Handler_Result]], Type[Matcher]] = {}
    runnings: set[RunningPackage] = set()

    @classmethod
    def get_command_handler(cls, package: CommandPackage[T_Handler_Result], matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent, Message], Awaitable[T_Handler_Result]]:
        if package.empty_handler:
            async def command_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> None:
                pass
        else:
            async def command_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> T_Handler_Result:
                logger.info(
                    "Run command handler: {name}",
                    name = package.component,
                )
                persona_info ,send_msg = await package.command_enter(bot, event, args, matcher)
                return await cls.enter_handler(package, persona_info, send_msg)
        return command_handler
    
    @classmethod
    def get_message_handler(cls, package: CommandPackage[T_Handler_Result], matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent], Awaitable[T_Handler_Result]]:
        if package.empty_handler:
            async def message_handler(bot: Bot, event: MessageEvent):
                pass
        else:
            async def message_handler(bot: Bot, event: MessageEvent) -> T_Handler_Result:
                logger.info(
                    "Run message handler: {name}",
                    name = package.component,
                )
                persona_info ,send_msg = await package.message_enter(bot, event, matcher)
                return await cls.enter_handler(package, persona_info, send_msg)
        return message_handler
    
    @classmethod
    async def enter_handler(cls, package: CommandPackage[T_Handler_Result], persona_info: PersonaInfo, send_msg: SendMsg) -> T_Handler_Result:
        try:
            logger.info(
                "Enter command from message: {message_id}",
                message_id = persona_info.message_id,
            )

            if not await package.permissions_check(persona_info, send_msg):
                logger.warning(
                    "Command {name} from message {message_id} has insufficient access",
                    name = package.component,
                    message_id = persona_info.message_id,
                )
                send_msg.break_handler()
            
            if package.superuser_permissions and not persona_info.is_superuser:
                await package.insufficient_access(persona_info, send_msg)
            
            if send_msg.is_debug_mode:
                await package.on_debug_mode(persona_info, send_msg)
            
            task = asyncio.create_task(
                package.handler(persona_info, send_msg)
            )
            running = RunningPackage(
                package = package,
                matcher = send_msg.matcher,
                persona_info = persona_info,
                send_msg = send_msg,
                task = task
            )
            cls.runnings.add(running)

            try:
                result = await task
                return result
            except asyncio.CancelledError:
                return await package.on_cancel(persona_info, send_msg)
            finally:
                cls.runnings.remove(running)
            
        except NoneBotException as e:
            return await package.on_nonebot_exception(e, persona_info, send_msg)
        except RepeaterException as e:
            return await package.on_repeater_exception(e, persona_info, send_msg)
        except Exception as e:
            return await package.on_error(e, persona_info, send_msg)
        except BaseException as e:
            return await package.on_interpreter_error(e, persona_info, send_msg)
        finally:
            await package.handler_exit(persona_info, send_msg)
    
    @classmethod
    async def horizontal_call(cls, package: Type[CommandPackage[T_Handler_Result]], persona_info: PersonaInfo, send_msg: SendMsg | None = None):
        package_instance = cls.commands[package]
        persona_info_copy, send_msg_copy = await package_instance.horizontal_enter(persona_info, send_msg)
        return await cls.enter_handler(package_instance, persona_info_copy, send_msg_copy)

    @classmethod
    def register(cls, package: Type[CommandPackage[T_Handler_Result]]) -> None:
        if package.enabled:
            try:
                package.on_before_instantiate()
                package_instance = package()
                matcher = package_instance.on_matcher_registered(
                    cls._get_matcher(package_instance)
                )
                    
                match package_instance.listen_type:
                    case ListenType.Command:
                        if storage_configs.log_registed_handler_name:
                            logger.info(
                                "Register command: {name}",
                                name = package_instance.component
                            )
                        handler = cls.get_command_handler(package_instance, matcher)
                    case ListenType.Message:
                        if storage_configs.log_registed_handler_name:
                            logger.info(
                                "Register command: {name}",
                                name = package_instance.component
                            )
                        handler = cls.get_message_handler(package_instance, matcher)
                    case _:
                        raise ValueError(f"{package_instance.listen_type} is not supported")
                
                matcher.append_handler(handler)
                cls.commands[package] = package_instance
                cls.matchers[package] = matcher
                package_instance.on_registed()
            except:
                package.on_reg_failed(*sys.exc_info())
        return package
    
    @classmethod
    def log_registed_info(cls):
        logger.info(
            "Registed {count} commands",
            count = len(cls.commands)
        )
        commands:dict[CmdTypes, int] = {}
        for package in cls.commands:
            if package.cmd_type not in commands:
                commands[package.cmd_type] = 0
            commands[package.cmd_type] += 1
        for cmd_type, count in commands.items():
            logger.info(
                "Repeater.{cmd_type} registed {count} commands",
                count = count,
                cmd_type = cmd_type.value
            )
    
    @classmethod
    def destroy(cls, package: Type[CommandPackage[T_Handler_Result]]):
        if package in cls.commands:
            package_instance = cls.commands.pop(package)
            matcher = cls.matchers.pop(package)

            logger.info(
                "Destroy command: {name}",
                name = package_instance.component
            )
            
            package_instance.on_destroy()
            matcher.destroy()
    
    @classmethod
    async def adestroy(cls, package: Type[CommandPackage[T_Handler_Result]]):
        if package in cls.commands:
            package_instance = cls.commands.pop(package)
            matcher = cls.matchers.pop(package)

            logger.info(
                "Async Destroy command: {name}",
                name = package_instance.component
            )
            
            await package_instance.on_adestroy()
            matcher.destroy()
    
    @staticmethod
    def _get_matcher(package: CommandPackage) -> Type[Matcher]:
        match package.listen_type:
            case ListenType.Command:
                matcher = on_command(
                    cmd = package.cmd,
                    rule = package.rule,
                    aliases = set(package.aliases) if isinstance(package.aliases, set) else None,
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