import httpx

from ._http_transport import http_transport
from ..client_net_configs import *
from pydantic import BaseModel
from ._response import Response
from ._namespace import Namespace
from ._ssl import get_ssl_context
from ..logger import logger

class RendedImage(BaseModel):
    image_url: str = ""
    file_uuid: str = ""
    style: str = ""
    timeout: float = 0.0
    text: str = ""
    created: float = 0.0
    created_ms: int = 0

class TextRender:
    _client = httpx.AsyncClient(
        base_url = BASE_URL,
        timeout = storage_configs.server_api_timeout.render,
        transport = http_transport,
        verify = get_ssl_context()
    )

    def __init__(self, namespace: str | Namespace, timeout:float = 60.0):
        self.url = BASE_URL
        if isinstance(namespace, str):
            self.namespce = namespace
        elif isinstance(namespace, Namespace):
            self.namespce = namespace.namespace_str
        else:
            raise TypeError(f"namespace must be str or Namespace, not {type(namespace)}")
        self._timeout = timeout

    async def render(
            self,
            text: str,
            direct_output: bool | None = None,
            document_bottom_comment: str = ""
        ) -> Response[RendedImage]:
        logger.info(
            "Render text:\n{text}",
            text = text,
            module = "text-render"
        )
        
        response = await self._client.post(
            f"{TEXT_RENDER_ROUTE}/{self.namespce}",
            json={
                "text": text,
                "direct_output": direct_output,
                "document_bottom_comment": document_bottom_comment
            },
            timeout = self._timeout
        )
        
        return Response(
            response,
            model = RendedImage
        )
        