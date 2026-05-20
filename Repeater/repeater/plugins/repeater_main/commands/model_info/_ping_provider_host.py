from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdType
)
from .._clients import ModelInfoClient, ModelInfo

@CommandCaller.register
class PingProviderHost(CommandPackage):
    cmd = "pingProviderHost"
    aliases = {
        "pph",
        "PPH",
        "ping_provider_host",
        "Ping_Provider_Host",
        "PingProviderHost",
        "PING_PROVIDER_HOST",
    }
    cmd_type = CmdType.MODEL

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        model_info_client = ModelInfoClient()

        response = await model_info_client.ping_provider(persona_info.namespace_str)
        if response.code == 200:
            ping_response = response.get_data()
            if ping_response is None:
                await send_msg.send_error("Error: No Model Data")
            else:
                text_buffer: list[str] = []
                text_buffer.append(f"Successful Times: {ping_response.successful}")
                text_buffer.append(f"Average Time Spent: {ping_response.average_time_spent}")
                for detail in ping_response.details:
                    for time in detail.time:
                        text_buffer.append(f"Ping [{detail.host}] in {time}ms")
                    text_buffer.append(f"Ping [{detail.host}] average inner {detail.average_time}ms")
                await send_msg.send_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response)