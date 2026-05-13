from ...assist import PersonaInfo, SendMsg
from ...command_register import CommandCaller, CommandPackage
from .._clients import RequestLogClient

@CommandCaller.register
class TokenCount(CommandPackage):
    cmd = "tokenCount"
    aliases = {
        "tc",
        "TC",
        "token_count",
        "Token_Count",
        "TokenCount",
        "TOKEN_COUNT",
    }

    @property
    def component(self) -> str:
        return f"Statistics.{self.__class__.__name__}"

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        client = RequestLogClient()

        request_logs = client.get_request_log()

        total_token_count = 0
        input_token_count = 0
        output_token_count = 0
        cache_hit_count = 0
        cache_miss_count = 0

        user_id = persona_info.namespace_str

        async for request_log in request_logs:
            if request_log.user_id == user_id:
                total_token_count += request_log.total_tokens
                input_token_count += request_log.prompt_tokens
                output_token_count += request_log.completion_tokens
                if request_log.cache_hit_count or request_log.cache_miss_count:
                    cache_hit_count += request_log.cache_hit_count
                    cache_miss_count += request_log.cache_miss_count
                else:
                    cache_miss_count += request_log.prompt_tokens
        
        await send_msg.send_prompt(
            f"Total Token Count: {total_token_count}\n"
            f"Input Token Count: {input_token_count}\n"
            f"Output Token Count: {output_token_count}\n"
            f"Cache Hit Count: {cache_hit_count}\n"
            f"Cache Miss Count: {cache_miss_count}\n"
            f"Cache Hit Rate: {cache_hit_count / (cache_hit_count + cache_miss_count):.2%}\n"
        )