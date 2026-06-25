import sys
import time
import asyncio
from .package import CommandPackage
from ..assist import PersonaInfo, SendMsg, Namespace
from ..cmd_info import CmdTypes
from ..client_configs import storage_configs
from ..exceptions import *
from nonebot.exception import NoneBotException
from typing import (
    Any,
    Type,
    Callable,
    Awaitable,
    TypeVar,
    NoReturn
)
from nonebot import on_command, on_message
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from .listen_type import ListenType
from nonebot import logger
from .running_package import RunningPackage
from .sub_cmd_breaked import SubCmdBreaked

T_Handler_Result = TypeVar("T_Handler_Result")

class CommandCaller:
    commands: dict[Type[CommandPackage[Any]], CommandPackage[Any]] = {}
    triggers: dict[str | tuple[str, ...], Type[CommandPackage[Any]]] = {}
    types: dict[CmdTypes, list[Type[CommandPackage[Any]]]] = {}
    matchers: dict[Type[CommandPackage[Any]], Type[Matcher]] = {}
    runnings: set[RunningPackage] = set()
    listen_message_tasks: dict[Namespace, set[asyncio.Future[PersonaInfo]]] = {}
    listen_lock: asyncio.Lock = asyncio.Lock()

    @staticmethod
    def delimiters() -> set[str]:
        return get_driver().config.command_sep
    
    @classmethod
    def get_instance(cls, package: Type[CommandPackage[T_Handler_Result]]) -> CommandPackage[T_Handler_Result]:
        """
        Get the instance of the command package.

        :param package: The command package.
        :return: The instance of the command package.
        """
        return cls.commands[package]

    @classmethod
    def get_command_handler(cls, package: CommandPackage[T_Handler_Result], matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent, Message], Awaitable[T_Handler_Result | Any | SubCmdBreaked | None | NoReturn]]:
        """
        Get the command handler.

        :param package: The command package.
        :param matcher: The matcher.
        :return: The command handler.
        """
        async def command_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> T_Handler_Result | Any | SubCmdBreaked | None | NoReturn:
            logger.info(
                "Run command handler: {name}",
                name = package.component,
            )
            persona_info ,send_msg = await package.command_enter(bot, event, args, matcher)
            return await cls.enter_handler(package, persona_info, send_msg)
        return command_handler
    
    @classmethod
    def get_message_handler(cls, package: CommandPackage[T_Handler_Result], matcher: Type[Matcher]) -> Callable[[Bot, MessageEvent], Awaitable[T_Handler_Result | Any | SubCmdBreaked | None | NoReturn]]:
        """
        Get the message handler.

        :param package: The command package.
        :param matcher: The matcher.
        :return: The message handler.
        """
        async def message_handler(bot: Bot, event: MessageEvent) -> T_Handler_Result | Any | SubCmdBreaked | None | NoReturn:
            logger.info(
                "Run message handler: {name}",
                name = package.component,
            )
            persona_info ,send_msg = await package.message_enter(bot, event, matcher)
            return await cls.enter_handler(package, persona_info, send_msg)
        return message_handler
    
    @classmethod
    async def wait_message(cls, namepsace: Namespace) -> PersonaInfo:
        """
        Wait for the message.

        :param package: The command package.
        :param task: The task.
        :return: None
        """
        future: asyncio.Future[PersonaInfo] = asyncio.get_event_loop().create_future()
        async with cls.listen_lock:
            cls.listen_message_tasks.setdefault(namepsace, set()).add(future)
        logger.info(
            "Create Wait Message Task: {future}",
            future = repr(future),
        )
        result = await future
        return result
    
    @classmethod
    async def enter_handler(cls, package: CommandPackage[T_Handler_Result], persona_info: PersonaInfo, send_msg: SendMsg) -> T_Handler_Result | Any | SubCmdBreaked | None | NoReturn:
        """
        Enter the message handler.

        :param package: The command package.
        :param persona_info: The persona info.
        :param send_msg: The send message function.
        :return: The result of the message handler.
        """
        result = await cls._enter_handler(
            package,
            persona_info,
            send_msg
        )
        if isinstance(result, type):
            if issubclass(result, SubCmdBreaked):
                result = result()
        
        logger.info(
            "Handler return: {result}({type})",
            result = repr(result),
            type = type(result).__name__,
        )
        return result
    
    @classmethod
    async def _enter_handler(cls, package: CommandPackage[T_Handler_Result], persona_info: PersonaInfo, send_msg: SendMsg) -> T_Handler_Result | Any | SubCmdBreaked | Type[SubCmdBreaked] | None | NoReturn:
        """
        Enter the message handler.

        :param package: The command package.
        :param persona_info: The persona info.
        :param send_msg: The send message function.
        :return: The result of the message handler.
        """
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
            
            if not await cls.check_acceptable_sources(package, persona_info):
                return await package.on_unacceptable_source(persona_info, send_msg)
            
            if package.superuser_permissions and not persona_info.is_superuser:
                return await package.insufficient_access(persona_info, send_msg)
            
            if send_msg.is_debug_mode:
                return await package.on_debug_mode(persona_info, send_msg)
            
            task: asyncio.Task[T_Handler_Result] = asyncio.create_task(
                coro = package.enter_handler(
                    persona_info = persona_info,
                    send_msg = send_msg
                )
            )
            running: RunningPackage[T_Handler_Result] = RunningPackage(
                start_time = time.time_ns(),
                start_monotonic_time = time.perf_counter_ns(),
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
    async def horizontal_call(
        cls,
        package: Type[CommandPackage[T_Handler_Result]] | CommandPackage[T_Handler_Result],
        persona_info: PersonaInfo,
        send_msg: SendMsg | None = None
    ) -> T_Handler_Result | Any | SubCmdBreaked | None | NoReturn:
        """
        Horizontal call handler

        :param package: CommandPackage
        :param persona_info: PersonaInfo
        :param send_msg: SendMsg
        :return: Handler result
        """
        if isinstance(package, type) and issubclass(package, CommandPackage):
            package_instance: CommandPackage[T_Handler_Result] = cls.commands[package]
        elif isinstance(package, CommandPackage):
            package_instance = package
        else:
            raise TypeError("package must be CommandPackage or subclass of CommandPackage")
        
        persona_info_copy, send_msg_copy = await package_instance.horizontal_enter(persona_info, send_msg)
        return await cls.enter_handler(package_instance, persona_info_copy, send_msg_copy)
    
    @staticmethod
    async def check_acceptable_sources(package: CommandPackage[T_Handler_Result], persona_info: PersonaInfo) -> bool:
        """
        Check if the persona is allowed to call the command

        :param package: CommandPackage
        :param persona_info: PersonaInfo
        :return: True if the persona is allowed to call the command, False otherwise
        """
        if package.acceptable_sources is None:
            return True
        return persona_info.source in package.acceptable_sources
    
    @classmethod
    def register(cls, package: Type[CommandPackage[T_Handler_Result]]) -> Type[CommandPackage[T_Handler_Result]]:
        """
        Register a command

        :param package: CommandPackage Type
        :return: CommandPackage Type
        """
        if package.enabled:
            register_start_time = time.perf_counter_ns()
            try:
                package.on_before_instantiate()
                if package in cls.commands:
                    package.on_duplicate_handler()
                package_instance = package()
                package_instance.__time_for_registed__ = time.time_ns()
                matcher = package_instance.on_matcher_registered(
                    cls._create_matcher(package_instance)
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
                cls._reg_package(
                    package = package,
                    package_instance = package_instance,
                    matcher = matcher
                )
                package_instance.on_registed()
            except:
                package.on_reg_failed(*sys.exc_info())
            register_end_time = time.perf_counter_ns()

            logger.info(
                "Register command {name} done, cost {cost:.3f} ms",
                name = package_instance.component,
                cost = (register_end_time - register_start_time) / 1e6
            )
        return package
    
    @classmethod
    def _reg_package(
        cls,
        package: Type[CommandPackage[T_Handler_Result]],
        package_instance: CommandPackage[T_Handler_Result],
        matcher: Type[Matcher]
    ) -> None:
        """
        Register package to resource pool
        """
        cls.commands[package] = package_instance
        cls.matchers[package] = matcher
        cls._reg_types(package_instance.cmd_type, package)
        if package_instance.listen_type == ListenType.Command:
            cls._reg_triggers(package_instance.cmd, package)
            if package_instance.aliases:
                for trigger in package_instance.aliases:
                    cls._reg_triggers(trigger, package)
    
    @classmethod
    def _reg_types(cls, cmd_type: CmdTypes, package: Type[CommandPackage[T_Handler_Result]]) -> None:
        """
        Register package to types pool
        """
        types_list = cls.types.setdefault(cmd_type, [])
        types_list.append(package)
    
    @classmethod
    def _reg_triggers(cls, trigger: str | tuple[str, ...], package: Type[CommandPackage[T_Handler_Result]]) -> None:
        """
        Register package to triggers pool
        """
        if trigger in cls.triggers:
            package.on_duplicate_trigger(trigger)
        cls.triggers[trigger] = package
    
    @classmethod
    def log_registed_info(cls) -> None:
        """
        Log registed info
        """
        total = len(cls.commands)
        logger.info(
            "Registed {count} commands",
            count = total
        )
        
        if total > 0:
            logger.info(
                "Repeater:"
            )
            for cmd_type, packages in cls.types.items():
                logger.info(
                    "  {cmd_type}({ratio:.2%})",
                    cmd_type = cmd_type,
                    ratio = len(packages) / total
                )
                for package in packages:
                    package_instance = cls.commands[package]
                    logger.info(
                        "    {name}",
                        name = package_instance.component,
                    )
    
    @classmethod
    def destroy(cls, package: Type[CommandPackage[T_Handler_Result]]) -> None:
        """
        Destroy a Handler

        :param package: The package of the Handler
        """
        if package in cls.commands:
            package_instance = cls.commands.pop(package)
            matcher = cls.matchers.pop(package)

            logger.info(
                "Destroy Handler: {name}",
                name = package_instance.component
            )
            
            package_instance.on_destroy()
            matcher.destroy()
    
    @classmethod
    async def adestroy(cls, package: Type[CommandPackage[T_Handler_Result]]) -> None:
        """
        Destroy a Handler on an async context
        
        :param package: The package of the Handler
        """
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
    def _create_matcher(package: CommandPackage) -> Type[Matcher]:
        """
        Create a matcher for a package

        :param package: The package of the Handler
        :return: The matcher
        """
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
    
    @classmethod
    async def report_message(cls, persona_info: PersonaInfo, send_msg: SendMsg):
        """
        Report a new message for processing.
        """
        namespace = persona_info.namespace
        if namespace in cls.listen_message_tasks:
            async with cls.listen_lock:
                futures = cls.listen_message_tasks.pop(namespace)
                for future in futures:
                    future.set_result(persona_info)
                