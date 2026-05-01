# 服务端配置
from ._net_config import net_config
from ._storage_configs import storage_configs

# ==== BASE URL ==== #
BASE_URL = net_config.backend_baseurl

# ==== CHAT API ==== #
CHAT_ROUTE = "/generate/chat/completion"
BREAK_CHAT_TASK_ROUTE = "/generate/chat/break"
GET_CHAT_BUFFER_ROUTE = "/generate/chat/buffer"

# ==== CONTEXT API ==== #
GET_CONTEXT_ROUTE = "/userdata/context/get"
GET_CONTEXT_LENGTH_ROUTE = "/userdata/context/length"
ROLE_STRUCTRUE_ROUTE = "/userdata/context/structure_check/role"
INJECT_CONTEXT_ROUTE = "/userdata/context/inject"
WIHTDRAW_CONTEXT_ROUTE = "/userdata/context/withdraw"

# ==== PROMPT API ==== #
SET_PROMPT_ROUTE = "/userdata/prompt/set"
GET_PROMPT_ROUTE = "/userdata/prompt/get"

# ==== CONFIG API ==== #
SET_CONFIG_ROUTE = "/userdata/config/set"
GET_CONFIG_ROUTE = "/userdata/config/get"
REMOVE_CONFIG_KEY_ROUTE = "/userdata/config/delkey"

# ==== MODEL API ==== #
GET_MODEL_UID_LIST = "/models"

# ==== Download User Data File ==== #
DOWNLOAD_USER_DATA_FILE_ROUTE = "/userdata/file"
PACKAGE_USER_SPACE_ROUTE = "/userdata/package_space"

# ==== RENDER API ==== #
TEXT_RENDER_ROUTE = "/render"

# ==== TEMPLATE RENDER API ==== #
TEMPLATE_RENDER = "/template/render"

# ==== VERSION API ==== #
VERSION_ROUTE = f"/version"

# ==== CONFIG ==== #
HELLO_CONTENT = storage_configs.hello_content
RepeaterDebugMode = net_config.repeater_debug_mode # 是否开启调试模式，调试模式下，将直接返回消息内容，而不进行后端访问操作

