from ...client_net_configs import storage_configs
from ..network.image_downloader import ImageDownloader
from nonebot.adapters.onebot.v11 import Message

async def get_images_url(message: Message, base64: bool | None = None) -> list[str]:
    if base64 is None:
        base64 = storage_configs.use_base64_image_url
    images: list[str] = []
    if "image" in message:
        async with ImageDownloader(
            message,
            timeout=storage_configs.download_image_timeout
        ) as downloader:
            if base64:
                get_image_url = downloader.download_image_to_base64()
                async for image_url in get_image_url:
                    if image_url is not None:
                        images.append(image_url)
            else:
                for image_url in downloader.get_images():
                    images.append(image_url)
    return images