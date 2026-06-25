from nonebot import logger
from nonebot import get_plugin_config
from pydantic import BaseModel, Field
from typing import Optional
from ._level import Level

class LoggerConfig(BaseModel):
    repeater_logger_level: Level = Field(Level.INFO)
    repeater_logger_format: str = Field("{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {extra[module]} - {message}")
    repeater_logger_path: str = Field("logs/repeater-log-{time:YYYY-MM-DD-HH-mm-ss}.log")
    repeater_logger_enable_queue: bool = Field(True)
    repeater_logger_delay: bool = Field(True)
    repeater_logger_rotation: str = Field("100 MB")
    repeater_logger_retention: str = Field("1 month")
    repeater_logger_compression: str = Field("zip")

logger_config = get_plugin_config(LoggerConfig)

# file
logger.add(
    logger_config.repeater_logger_path,
    level = logger_config.repeater_logger_level.value,
    format = logger_config.repeater_logger_format,
    enqueue = logger_config.repeater_logger_enable_queue,
    delay = logger_config.repeater_logger_delay,
    rotation = logger_config.repeater_logger_rotation,
    retention = logger_config.repeater_logger_retention,
    compression = logger_config.repeater_logger_compression,
)

logger.configure(
    extra={
        "module": "[System]"
    }
)