# 服务端配置
from ._net_config import net_config
from ._storage_configs import storage_configs

# ==== BASE URL ==== #
BASE_URL = net_config.backend_baseurl

# ==== CHAT API ==== #
CHAT_ROUTE = f"/chat/completion"
BREAK_CHAT_TASK_ROUTE = f"/chat/break"
GET_CHAT_BUFFER_ROUTE = f"/chat/buffer"

# ==== CONTEXT API ==== #
GET_CONTEXT_ROUTE = "/userdata/context/get"
GET_CONTEXT_LENGTH_ROUTE = "/userdata/context/length"
ROLE_STRUCTRUE_ROUTE = "/userdata/context/structure_check/role"
INJECT_CONTEXT_ROUTE = "/userdata/context/inject"
WIHTDRAW_CONTEXT_ROUTE = "/userdata/context/withdraw"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = "/userdata/prompt/set"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = "/userdata/config/set"
GET_CONFIG_ROUTE = "/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = "/userdata/config/delkey"

# ==== MODEL API ==== #
GET_MODEL_UID_LIST = "/model/list"
GET_MODEL_INFO = "/model/info"
GET_MODEL_TYPES = "/model/types"

# ==== Download User Data File ==== #

DOWNLOAD_USER_DATA_FILE_ROUTE = "/userdata/file"

# ==== RENDER API ==== #
TEXT_RENDER_ROUTE = "/render"

# ==== VARIABLE EXPANSION API ==== #
VARIABLE_EXPANSION = "/variable_expand"

# ==== VERSION API ==== #
VERSION_ROUTE = f"/version"

# ==== CONFIG ==== #
HELLO_CONTENT = storage_configs.hello_content
RepeaterDebugMode = net_config.repeater_debug_mode # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

