import time as _time
from nonebot import logger as _logger

start_import_time = _time.perf_counter_ns()

# === Chat === #
from .commands.chat import *

# === Context === #
from .commands.context import *

# === Prompt === #
from .commands.prompt import *

# === Config === #
from .commands.config import *

# === Mixed === #
from .commands.mixed import *

# === Model Info === #
from .commands.model_info import *

# === Status === #
from .commands.status import *

# === Licenses === #
from .commands.licenses import *

# === More Interesting Tools === #
from .commands.more_interesting_tools import *

# === Nexus === #
from .commands.nexus import *

# === Var Expand === #
from .commands.variable_expansion import *

# === UserDataFile === #
from .commands.user_file import *

# === SessionID === #
from .commands.get_namespace import handle_get_namespace

# === TextRender === #
from .commands.text_render import handle_text_render

# === Comment === #
from .commands.annotation import handle_annotation

# === Adaptation === #
from .commands.adaptation import handle_adaptation

# === Calculate Length Score === #
from .commands.calculate_length_score import handle_calculate_length_score

# === Send Any Message === #
from .commands.send_msg import handle_send_message

# === Adaptation Info === #
from ._adaptation_info import __adaptation__, __adaptation_text__

end_import_time = _time.perf_counter_ns()
_logger.info(
    "Import time: {import_time:.2f}s",
    import_time = (end_import_time - start_import_time) / 1e9
)