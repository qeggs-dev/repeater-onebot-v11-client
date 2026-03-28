import orjson
from typing import (
    Any,
    AsyncIterator
)
import httpx
from .._content_role import ContentRole
from ._response_body import ChatResponse, StreamChatChunkResponse
from ._break_response_body import BreakResponse
from ._cross_user_data_routing import CrossUserDataRouting
from ....exit_register import ExitRegister
from ....assist import PersonaInfo, Response
from ....core_net_configs import *
from ._request_model import ChatRequestModel, ChatUserInfo, AdditionalData
from ...._adaptation_info import __adaptation__, __adaptation_text__

exit_register = ExitRegister()

class ChatCore:
    _chat_client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.chat
    )
    
    def __init__(self, persona_info: PersonaInfo, namespace: str | None = None):
        self._persona_info = persona_info
        self._namespace = namespace
    
    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace
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
        add_metadata: bool = True,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_uid: str | None = None,
        thinking: bool | None = None,
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
    ) -> Response[ChatResponse]:
        """
        发送消息到AI后端
        
        :param message: 消息内容
        :param add_metadata: 是否添加元数据
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示
        :param model_uid: 模型UID
        :param thinking: 思考模式
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
            user_info = ChatUserInfo(
                username = self._persona_info.nickname,
                nickname = self._persona_info.card,
                gender = self._persona_info.gender,
                age = self._persona_info.age,
            ),
            add_metadata = add_metadata,
            role_name = role_name,
            temporary_prompt = temporary_prompt,
            model_uid = model_uid,
            thinking = thinking,
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
        try:
            response = await self._chat_client.post(
                url = url,
                json = data.submit_body()
            )
        except Exception as e:
            return Response(model=ChatResponse)
        return Response(
            response,
            ChatResponse
        )
    
    async def send_stream_message(
        self,
        message: str,
        add_metadata: bool = True,
        role_name: str | None = None,
        temporary_prompt: str | None = None,
        model_uid: str | None = None,
        thinking: bool | None = None,
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
    ) -> AsyncIterator[Any]:
        """
        发送消息到AI后端，并获取流式响应
        
        :param message: 消息内容
        :param add_metadata: 是否添加元数据
        :param role_name: 角色名称
        :param temporary_prompt: 临时提示
        :param model_uid: 模型UID
        :param thinking: 思考模式
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
        self._add_extra_template_fields(extra_template_fields)
        data = ChatRequestModel(
            message = message,
            user_info = ChatUserInfo(
                username = self._persona_info.nickname,
                nickname = self._persona_info.card,
                gender = self._persona_info.gender,
                age = self._persona_info.age,
            ),
            add_metadata = add_metadata,
            role_name = role_name,
            temporary_prompt = temporary_prompt,
            model_uid = model_uid,
            thinking = thinking,
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
            stream = True,
        )
        async with self._chat_client.stream(
            method="POST",
            url=url,
            json=data.submit_body()
        ) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if not line.strip():
                    continue

                yield StreamChatChunkResponse(**orjson.loads(line))
    
    async def break_chat_task(self) -> Response[BreakResponse]:
        """
        中断当前在线的任务
        """
        try:
            response = await self._chat_client.post(
                url = f"{BREAK_CHAT_TASK_ROUTE}/{self.namespace}"
            )
        except Exception as e:
            return Response(model=BreakResponse)

        return Response(
            httpx_response = response,
            model = BreakResponse
        )
     
    
    exit_register.register()
    async def close(self):
        await self._chat_client.aclose()
    # endregion