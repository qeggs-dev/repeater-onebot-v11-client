import re
import httpx
import asyncio

from typing import (
    Any
)
from ._chat_buffer import ChatBufferResponse
from .._content_role import ContentRole
from ._response_body import ChatResponse
from ._break_response_body import BreakResponse
from ._cross_user_data_routing import CrossUserDataRouting
from ...exit_register import ExitRegister
from ...assist import PersonaInfo, Namespace, Response, http_transport, CmdTypes
from ...client_net_configs import *
from ._request_model import ChatRequestModel, ChatUserInfo, AdditionalData
from ..._adaptation_info import __adaptation__, __adaptation_text__
from ...logger import logger as base_logger
from ...exceptions import BreakWithErrorMessage

logger = base_logger.bind(module = "chat_client")

exit_register = ExitRegister()

class ChatClient:
    _chat_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.chat,
        transport = http_transport
    )
    metadata_pattern = re.compile(r"> Message\s*?Metadata:.*?---(?:\r?\n)+", re.DOTALL | re.IGNORECASE)
    
    def __init__(self, persona_info: PersonaInfo, namespace: str | Namespace | None = None):
        self._persona_info = persona_info
        self._namespace = namespace
    
    @property
    def namespace(self) -> str:
        if self._namespace is not None:
            if isinstance(self._namespace, Namespace):
                return self._namespace.namespace_str
            elif isinstance(self._namespace, str):
                return self._namespace
            else:
                raise TypeError(f"Invalid type for namespace: {type(self._namespace).__name__}")
        else:
            return self._persona_info.namespace_str
    
    @property
    def merge_namespace(self) -> str | None:
        if storage_configs.usage_group_context:
            return self._persona_info.namespace.merge_namespace
        return None
    
    def _add_extra_template_fields(self, extra_template_fields: dict[str, Any] | None = None) -> dict[str, Any]:
        if extra_template_fields is None:
            extra_template_fields_copy = {}
        else:
            extra_template_fields_copy = extra_template_fields.copy()
        extra_template_fields_copy.update(
            {
                "message_type": self._persona_info.source.value,
                "adaptation_version": __adaptation__,
                "adaptation_info": __adaptation_text__,
            }
        )
        return extra_template_fields_copy
    
    async def send_message(
        self,
        message: str | None = None,
        suffix: str | None = None,
        echo: bool | None = None,
        fim_mode: bool | None = None,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_id: str | None = None,
        thinking: bool | None = None,
        allow_tool_calls: bool | None = None,
        extra_template_fields: dict[str, Any] | None = None,
        image_url: str | list[str] | None = None,
        video_url: str | list[str] | None = None,
        audio_url: str | list[str] | None = None,
        file_url: str | list[str] | None = None,
        load_prompt: bool | None = None,
        save_context: bool | None = None,
        save_new_only: bool | None = None,
        history_msg_role_map: dict[ContentRole, ContentRole | None] | None = None,
        cross_user_data_routing: CrossUserDataRouting | None = None,
        continue_completion: bool | None = None,
        timeout: int | float | None = None,
        add_metadata: bool = True,
    ) -> Response[ChatResponse]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param add_metadata: 是否添加元数据
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示
        :param model_id: 模型UID
        :param thinking: 思考模式
        :param allow_tool_calls: 是否允许工具调用
        :param extra_template_fields: 额外模板字段
        :param image_url: 图片URL
        :param video_url: 视频URL
        :param audio_url: 音频URL
        :param file_url: 文件URL
        :param load_prompt: 是否加载提示
        :param save_context: 是否保存上下文
        :param save_new_only: 是否只保存新内容
        :param history_msg_role_map: 历史消息角色映射
        :param cross_user_data_routing: 跨用户数据路由
        :param continue_completion: 是否继续生成
        :return: AI返回的消息
        """
        url = f"{CHAT_ROUTE}/{self.namespace}"

        if cross_user_data_routing is None:
            if self.merge_namespace:
                cross_user_data_routing = CrossUserDataRouting()
                cross_user_data_routing.context.fill_missing(self.merge_namespace)
        extra_template_fields = self._add_extra_template_fields(extra_template_fields)
        data = ChatRequestModel(
            message = message,
            suffix = suffix,
            echo = echo,
            fim_mode = fim_mode,
            user_info = ChatUserInfo(
                username = self._persona_info.nickname,
                nickname = self._persona_info.card,
                gender = self._persona_info.gender,
                age = self._persona_info.age,
            ),
            add_metadata = add_metadata,
            role_name = role_name,
            temporary_prompt = temporary_prompt,
            model_id = model_id,
            thinking = thinking,
            allow_tool_calls = allow_tool_calls,
            extra_template_fields = extra_template_fields,
            additional_data = AdditionalData(
                image_url = image_url,
                video_url = video_url,
                audio_url = audio_url,
                file_url = file_url,
            ),
            load_prompt = load_prompt,
            save_context = save_context,
            save_new_only = save_new_only,
            history_msg_role_map = history_msg_role_map,
            cross_user_data_routing = cross_user_data_routing,
            continue_completion = continue_completion,
        )
        if timeout is None:
            timeout = storage_configs.model_first_chunk_timeout
        
        task = asyncio.create_task(
            self._chat_client.post(
                url = url,
                json = data.submit_body()
            )
        )
        last_buffer_length: int | None = None
        if timeout is not None:
            while True:
                try:
                    response = await asyncio.wait_for(task, timeout = timeout)
                    break
                except asyncio.TimeoutError:
                    buffer_response = await self.get_chat_buffer()
                    if buffer_response:
                        buffer = buffer_response.get_data()
                        if buffer is not None:
                            if last_buffer_length is None:
                                last_buffer_length = len(buffer)
                                if last_buffer_length == 0:
                                    await self.break_chat_task()
                                    raise BreakWithErrorMessage("The build task has been actively aborted because the buffer did not find anything.")
                            else:
                                now_buffer_length = len(buffer)
                                if now_buffer_length == last_buffer_length:
                                    await self.break_chat_task()
                                    raise BreakWithErrorMessage("The build task has been actively aborted because this check buffer is the same length as the last time.")
                                else:
                                    last_buffer_length = now_buffer_length
        response = await task
        
        return Response(
            response,
            ChatResponse
        )
    
    async def break_chat_task(self) -> Response[BreakResponse]:
        """
        中断当前在线的任务
        """
        try:
            response = await self._chat_client.post(
                url = f"{BREAK_CHAT_TASK_ROUTE}/{self.namespace}"
            )
        except Exception as e:
            logger.error(
                "Error sending message to chat core: {error}",
                error = e
            )
            return Response(model=BreakResponse)

        return Response(
            httpx_response = response,
            model = BreakResponse
        )
    
    async def get_chat_buffer(self) -> Response[ChatBufferResponse]:
        """
        获取当前聊天缓冲区
        """
        try:
            response = await self._chat_client.get(
                url = f"{GET_CHAT_BUFFER_ROUTE}/{self.namespace}"
            )
        except Exception as e:
            logger.error(
                "Error sending message to chat core: {error}",
                error = e
            )
            return Response(model=ChatBufferResponse)

        return Response(
            httpx_response = response,
            model = ChatBufferResponse
        )
    
    exit_register.register()
    async def close(self):
        await self._chat_client.aclose()
    # endregion