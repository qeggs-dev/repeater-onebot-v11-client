import base64
from typing import AsyncGenerator
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ImageClient, ImagesResponse
from ...logger import logger

@CommandCaller.register
class GenerateImageStream(CommandPackage):
    cmd = "generateImageStream"
    aliases = {
        "gis",
        "GIS",
        "generate_image_stream",
        "Generate_Image_Stream",
        "GenerateImage_Stream",
        "GENERATE_IMAGE_STREAM",
    }
    cmd_type = CmdTypes.GENIMG

    async def get_client(self, persona_info: PersonaInfo) -> ImageClient:
        user_configs = await persona_info.get_user_configs()
        return ImageClient(persona_info, user_configs)
    
    async def get_prompt(self, persona_info: PersonaInfo, send_msg: SendMsg) -> str:
        text = persona_info.message_striped_str
        if not text:
            await send_msg.send_error("Error: No prompt provided")
        return text
    
    async def get_images(self, prompt: str, image_client: ImageClient, send_msg: SendMsg) -> AsyncGenerator[bytes, None]:
        stream = image_client.generate_stream(
            prompt = prompt,
        )
        async for image in stream:
            image_base64 = image.b64_json
            if image_base64:
                image_data = base64.b64decode(image_base64)
                yield image_data

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        image_client = await self.get_client(persona_info)
        prompt = await self.get_prompt(persona_info, send_msg)
        images = self.get_images(prompt, image_client, send_msg)
        async for image in images:
            await send_msg.send_images(
                image,
                continue_handler = True
            )
        send_msg.break_handler()