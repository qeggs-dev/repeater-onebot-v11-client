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

# === Statistics === #
from .commands.statistics import *

# === Licenses === #
from .commands.licenses import *

# === More Interesting Tools === #
from .commands.more_interesting_tools import *

# === Nexus === #
from .commands.nexus import *

# === Var Expand === #
from .commands.template_render import *

# === UserDataFile === #
from .commands.user_file import *

# === SessionID === #
from .commands.get_namespace import GetNamespace

# === TextRender === #
from .commands.markdown_render import TextRender

# === Comment === #
from .commands.annotation import Annotation

# === Adaptation === #
from .commands.adaptation import AdaptationInfo

# === Calculate Length Score === #
from .commands.calculate_length_score import CalculateLengthScore

# === Send Any Message === #
from .commands.send_msg import SendMessage

# === Adaptation Info === #
from ._adaptation_info import __adaptation__, __adaptation_text__