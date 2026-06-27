from ...client_configs import *
from ..response.response import Response
from .response import RendedImage
from ..base_client import BaseClient

class TextRender(BaseClient):
    timeout = storage_configs.server_api_timeout.render
    
    async def render(
            self,
            text: str,
            direct_output: bool | None = None,
            document_bottom_comment: str = ""
        ) -> Response[RendedImage]:
        response = await self.client.post(
            self.join_url_static(TEXT_RENDER_ROUTE, self.namespace),
            json={
                "text": text,
                "direct_output": direct_output,
                "document_bottom_comment": document_bottom_comment
            }
        )
        
        return Response(
            response,
            model = RendedImage
        )
        