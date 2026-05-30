import curlify2

from httpx import AsyncHTTPTransport, Request, Response
from loguru import logger

class HTTPTransport(AsyncHTTPTransport):
    async def handle_async_request(self, request: Request) -> Response:
        curlify = curlify2.Curlify(request)
        logger.info(
            "Sending request: \n{curl_str}\n",
            curl_str = curlify.to_curl(),
        )
        return await super().handle_async_request(request)

http_transport = HTTPTransport()