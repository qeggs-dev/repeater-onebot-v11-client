import curlify2

from httpx import AsyncBaseTransport, Request, Response
from loguru import logger

class AsyncHTTPTransport(AsyncBaseTransport):
    async def handle_async_request(self, request: Request) -> Response:
        curlify = curlify2.Curlify(request)
        logger.info(
            "Sending request: {curl_str}",
            curl_str = curlify.to_curl(),
        )
        return await super().handle_async_request(request)