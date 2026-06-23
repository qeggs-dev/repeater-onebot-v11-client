import json
import httpx
from typing import (
    Optional,
    Union
)

from urllib.parse import urljoin
from ...client_net_configs import *
from ...assist import Response, BaseClient
from ._request import ImagesRequest
from ._response import ImagesResponse
from .auxiliary import (
    Background,
    Moderation,
    OutputFormat,
    Quality,
    ImageResponseFormat,
    ImageSize,
    ImageStyle
)

class ImageClient(BaseClient):
    timeout = storage_configs.server_api_timeout.image

    async def generate(
            self,
            model_id: str | list[str] | None = None,
            prompt: str = "",
            
            background: Background | None = None,
            moderation: Moderation | None = None,
            n: int | None = None,
            output_compression: int | None = None,
            output_format: OutputFormat | None = None,
            partial_images: int | None = None,
            quality: Quality | None = None,
            response_format: ImageResponseFormat | None = None,
            size: ImageSize | str | None = None,
            stream: bool = False,
            style: ImageStyle | None = None,
            user: str | None = None,
        ) -> Response[ImagesResponse]:
        """Generate images from a prompt."""

        request = ImagesRequest(
            model_id = model_id,
            prompt = prompt,

            background = background,
            moderation = moderation,
            n = n,
            output_compression = output_compression,
            output_format = output_format,
            partial_images = partial_images,
            quality = quality,
            response_format = response_format,
            size = size,
            stream = stream,
            style = style,
            user = user,
        )
        response = await self.client.post(
            url = urljoin(IMAGE_ROUTE, self.namespace),
            json = request.model_dump(),
        )
        return Response(
            httpx_response = response,
            model = ImagesResponse
        )