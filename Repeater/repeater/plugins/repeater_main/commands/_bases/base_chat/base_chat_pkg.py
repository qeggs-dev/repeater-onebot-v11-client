from typing import NoReturn, ClassVar
from itertools import chain

from ....logger import logger
from ....clients import ChatClient, ChatSendMsg, ChatResponse
from ....assist import PersonaInfo, SendMsg, Response
from ....cmd_info import CmdTypes
from ....client_net_configs import storage_configs
from ....command_register import CommandPackage
from .message import SendMessage

class BaseChat(CommandPackage):
    cmd_type = CmdTypes.CHAT
    empty_exit: ClassVar[bool] = True
    no_input: ClassVar[bool] = False

    async def empty_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ):
        logger.warning("Message is empty")
        if self.empty_exit:
            send_msg.break_handler()
    
    async def parse_forward_msgs(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> str:
        forward_msgs = await persona_info.get_forward_msgs()
        if forward_msgs:
            forward_msgs_text = persona_info.generates_text_from_messages_list(forward_msgs)
            message_text = f"Forwarded messages:\n{forward_msgs_text}\n\n---\n\n{message_text}"
        else:
            message_text = ""
        
        return message_text
    
    @staticmethod
    async def open_file(
        persona_info: PersonaInfo,
        reply_msgs_texts: list[str],
        files_list: list[list[str]],
        file_ids: list[str]
    ):
        not_open_files: list[str] = []
        for file_id in file_ids:
            info = await persona_info.get_file_info(file_id)
            name = info.file_name
            size = int(info.file_size)

            if storage_configs.max_text_file_size is not None:
                if size > storage_configs.max_text_file_size:
                    logger.warning(
                        "File {name} is too large to open as text file",
                        name = name
                    )
                    not_open_files.append(name)
                    continue
            try:
                file_data = await persona_info.open_text_file(
                    file_id,
                    storage_configs.text_file_encoding
                )
                reply_msgs_texts.append(
                    f"[File {name}]\n[File Content Begin]{file_data}\n[File Content End]"
                )
                logger.info(
                    "File {name} was opened successfully",
                    name = name
                )
            except UnicodeDecodeError:
                logger.warning(
                    "File {name} was not opened",
                    name = name
                )
                not_open_files.append(file_id)
        
        files_list.append(not_open_files)
    
    async def parse_input(self, persona_info: PersonaInfo) -> str:
        message_text = persona_info.message_striped_str
        return message_text

    async def parse_message(
        self,
        persona_info: PersonaInfo,
        send_msg: SendMsg,
    ) -> SendMessage:
        if self.no_input:
            return SendMessage()
        else:
            message = persona_info.message
            if not persona_info:
                await self.empty_message(persona_info, send_msg)
            
            message_text = await self.parse_input(persona_info)

            message_text += await self.parse_forward_msgs(persona_info, send_msg)

            images: list[str] = await persona_info.get_images_url()
            audios: list[str] = persona_info.get_audio_url()
            videos: list[str] = persona_info.get_video_url()
            files: list[str] = persona_info.get_file_ids()

            images_list: list[list[str]] = [images]
            audios_list: list[list[str]] = [audios]
            videos_list: list[list[str]] = [videos]
            files_list: list[list[str]] = []
            
            reply_msgs = persona_info.from_reference_chain()
            reply_msgs_texts: list[str] = []
            
            await self.open_file(
                persona_info,
                reply_msgs_texts,
                files_list,
                files
            )
            
            async for msg in reply_msgs:
                if msg.is_self:
                    break

                forward_msgs_text = await self.parse_forward_msgs(msg, send_msg)
                if forward_msgs_text:
                    reply_msgs_texts.append(forward_msgs_text)
                reply_msgs_texts.append(msg.message_striped_str)
                reply_msgs_images: list[str] = await msg.get_images_url()
                reply_msgs_audios: list[str] = msg.get_audio_url()
                reply_msgs_videos: list[str] = msg.get_video_url()
                reply_msgs_files: list[str] = msg.get_file_ids()

                images_list.append(reply_msgs_images)
                audios_list.append(reply_msgs_audios)
                videos_list.append(reply_msgs_videos)
                await self.open_file(
                    msg,
                    reply_msgs_texts,
                    files_list,
                    reply_msgs_files
                )

            reply_msgs_text = "\n\n".join(reversed(reply_msgs_texts))
            reply_msgs_text = reply_msgs_text.replace("\n", "\n> ")

            if reply_msgs_text:
                if message_text:
                    message_text = f"Reply messages:\n{reply_msgs_text}\n\n---\n\n{message_text}"
                else:
                    message_text = reply_msgs_text
            
            # 恢复消息顺序
            images = list(chain.from_iterable(reversed(images_list)))
            audios = list(chain.from_iterable(reversed(audios_list)))
            videos = list(chain.from_iterable(reversed(videos_list)))

            if not (message_text or images or audios or videos):
                message_text = str(message)
            
            return SendMessage(
                text = message_text,
                images = images,
                audios = audios,
                videos = videos
            )

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        logger.info(
            "Received a message {message} from {namespace}",
            message = persona_info.message_striped_str,
            namespace = persona_info.namespace_str,
            module = send_msg.component
        )
        
        client = await self.get_client(persona_info)

        message = await self.parse_message(persona_info, send_msg)

        response = await self.send_message(
            client = client,
            images = message.images,
            audios = message.audios,
            videos = message.videos,
            message = message.text,
            persona_info = persona_info,
            send_msg = send_msg
        )

        if not response and response.initialized:
            await send_msg.send_error_response(
                response = response,
            )

        chat_send_msg = ChatSendMsg(
            component = send_msg.component,
            persona_info = persona_info,
            matcher = send_msg.matcher,
            response = response,
            reasoning_content_handler = self.reason_filters,
            content_handler = self.filters
        )
        await self.send_chat_send_msg(chat_send_msg)
    
    def filters(self, text: str) -> str:
        return text
    
    def reason_filters(self, text: str) -> str:
        return text
    
    async def get_client(self, persona_info: PersonaInfo) -> ChatClient:
        user_configs = await persona_info.get_user_configs()
        client = ChatClient(persona_info, user_configs)
        return client
    
    async def send_message(
        self,
        client: ChatClient,
        images: list[str],
        audios: list[str],
        videos: list[str],
        message: str,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> Response[ChatResponse]:
        response: Response[ChatResponse] = await client.send_message(
            message = message,
            image_url = images,
            audio_url = audios,
            video_url = videos,
        )
        return response
    
    async def send_chat_send_msg(self, chat_send_msg: ChatSendMsg) -> NoReturn:
        await chat_send_msg.send()