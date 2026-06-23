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
class GenerateImage(CommandPackage):
    cmd = "generateImage"
    aliases = {
        "gi",
        "GI",
        "generate_image",
        "Generate_Image",
        "GenerateImage",
        "GENERATE_IMAGE",
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
    
    async def get_images(self, prompt: str, image_client: ImageClient, send_msg: SendMsg) -> list[bytes]:
        response = await image_client.generate(
            prompt = prompt,
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
        prompt = await self.get_prompt(persona_info, send_msg)
        images = await self.get_images(prompt, image_client, send_msg)
        await send_msg.send_images(*images)