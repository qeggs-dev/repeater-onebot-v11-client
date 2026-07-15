# === Start Time === #
from .start_time import *

# === Commands === #
from . import commands as _commands

# === Adaptation Info === #
from ._adaptation_info import __adaptation__, __adaptation_text__

from .command_register import CommandCaller as _CommandCaller

# === Log Warn === #
from ._log_warn import warning_handler

_CommandCaller.log_registed_info()