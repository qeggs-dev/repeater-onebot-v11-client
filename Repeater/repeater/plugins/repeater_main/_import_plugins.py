# === Start Time === #
from .start_time import *

# === Commands === #
from .commands import *

# === Adaptation Info === #
from ._adaptation_info import __adaptation__, __adaptation_text__

from .command_register import CommandCaller as _CommandCaller

_CommandCaller.log_registed_info()