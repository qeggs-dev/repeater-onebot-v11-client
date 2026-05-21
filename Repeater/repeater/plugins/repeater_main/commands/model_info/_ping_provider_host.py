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
        model_uid = persona_info.message_striped_str
        if not model_uid:
            model_uid = None

        response = await model_info_client.ping_provider(
            persona_info.namespace_str,
            model_uid = model_uid
        )
        if response.code == 200:
            ping_response = response.get_data()
            if ping_response is None:
                await send_msg.send_error("Error: No Model Data")
            else:
                text_buffer: list[str] = []
                text_buffer.append(f"Successful Times: {ping_response.success_count}")
                text_buffer.append(f"Average Time Spent: {ping_response.average_time_spent}")
                for detail in ping_response.details:
                    statistics = detail.to_statistics()
                    text_buffer.append("")
                    text_buffer.append(f"**Host** [{detail.ip}]:")
                    text_buffer.append(f"**names:**")
                    for name in detail.host_names:
                        text_buffer.append(f"  - `{name}`")
                    text_buffer.append(f"**times:**")
                    for time in detail.time:
                        text_buffer.append(f"  - {time}")
                    text_buffer.append(f"**packet loss:** {detail.packet_loss}")
                    text_buffer.append(f"**max time:** {statistics.max}")
                    text_buffer.append(f"**min time:** {statistics.min}")
                    text_buffer.append(f"**avg time:** {statistics.mean}")
                    text_buffer.append(f"**median time:** {statistics.median}")
                    text_buffer.append(f"**standard deviation:** {statistics.std}")
                    text_buffer.append(f"**variance:** {statistics.var}")
                    text_buffer.append(f"**coefficient of variation:** {statistics.cv}")
                await send_msg.send_render_prompt("\n".join(text_buffer))
        else:
            await send_msg.send_response_check_code(response)