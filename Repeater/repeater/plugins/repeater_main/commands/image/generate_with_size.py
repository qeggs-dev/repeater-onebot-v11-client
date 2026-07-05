import re
import base64
from ...assist import PersonaInfo, SendMsg
from ...cmd_info import CmdTypes
from ...command_register import(
    CommandCaller,
    CommandPackage
)
from ...clients import ImageClient, ImagesResponse
from ...logger import logger

@CommandCaller.register
class GenerateImageWithSize(CommandPackage):
    cmd = "generateImageWithSize"
    aliases = {
        "giz",
        "GIZ",
        "generate_image_with_size",
        "Generate_Image_With_Size",
        "GenerateImageWithSize",
        "GENERATE_IMAGE_WITH_SIZE",
    }
    cmd_type = CmdTypes.GENIMG

    pattern = re.compile(r"^(?P<size>\d+?x\d+)\s*?(?P<prompt>.*)$", re.DOTALL)

    async def get_client(self, persona_info: PersonaInfo) -> ImageClient:
        user_configs = await persona_info.get_user_configs()
        return ImageClient(persona_info, user_configs)
    
    async def get_prompt(self, persona_info: PersonaInfo, send_msg: SendMsg) -> tuple[str, str]:
        text = persona_info.message_striped_str
        if not text:
            await send_msg.send_error("Error: No prompt provided")
        
        matched = self.pattern.match(text)
        if matched is None:
            await send_msg.send_error("Error: Invalid prompt format")
            send_msg.break_handler()
        
        size = matched.group("size")
        prompt = matched.group("prompt")

        assert isinstance(size, str), "size must be a string"
        assert isinstance(prompt, str), "prompt must be a string"

        return prompt, size
    
    async def get_images(self, prompt: str, size: str, image_client: ImageClient, send_msg: SendMsg) -> list[bytes]:
        response = await image_client.generate(
            prompt = prompt,
            size = size,
        )

        if response:
            data = response.get_data()
            if data is None:
                await send_msg.send_error_response(response)
            else:
                images: list[bytes] = []
                if data.data:
                    for index, image in enumerate(data.data):
                        if image.b64_json is not None:
                            images.append(
                                base64.b64decode(image.b64_json)
                            )
                        else:
                            logger.warning(
                                "No image data found in response[{index}].",
                                index = index
                            )
                    return images
                else:
                    await send_msg.send_error("No image data found in response.")
        else:
            await send_msg.send_error_response(response)

        assert False, "This line is never reached"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        image_client = await self.get_client(persona_info)
        prompt, size = await self.get_prompt(persona_info, send_msg)
        images = await self.get_images(prompt, size, image_client, send_msg)
        await send_msg.send_images(*images)