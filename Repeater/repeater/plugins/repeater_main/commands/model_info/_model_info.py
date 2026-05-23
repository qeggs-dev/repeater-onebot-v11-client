from ...assist import PersonaInfo, SendMsg
from ...command_register import(
    CommandCaller,
    CommandPackage,
    CmdTypes
)
from .._clients import ModelInfoClient, ModelInfo

@CommandCaller.register
class GetModelList(CommandPackage):
    cmd = "getModelList"
    aliases = {
        "gml",
        "GML",
        "get_model_list",
        "Get_Model_List",
        "GetModelList",
        "GET_MODEL_LIST",
    }
    cmd_type = CmdTypes.MODEL

    async def handler(self, persona_info: PersonaInfo, send_msg: SendMsg):
        if send_msg.is_debug_mode:
            await send_msg.send_debug_mode()

        model_info_client = ModelInfoClient()
        model_uid = persona_info.message_striped_str

        response = await model_info_client.get_models(model_uid)
        if response.code == 200:
            model_info = response.get_data()
            if model_info is None:
                await send_msg.send_error("Error: No Model Data")
            else:
                model_maps: dict[str, list[ModelInfo]] = {}
                for model in model_info.models:
                    if model.parent_id not in model_maps:
                        model_maps[model.parent_id] = []
                    model_maps[model.parent_id].append(model)

                text_buffer: list[str] = []
                for parent_id, models in model_maps.items():
                    sub_buffer: list[str] = []
                    sub_buffer.append(f"### {parent_id}")
                    sub_buffer.append("")
                    for model in models:
                        sub_buffer.append(f"**{model.name}**")
                        sub_buffer.append(f"  - uid: `{model.uid}`")
                        sub_buffer.append(f"  - parent: `{model.parent}`")
                        sub_buffer.append(f"  - parent_id: `{model.parent_id}`")
                        sub_buffer.append(f"  - timeout: {model.timeout}")
                    text_buffer.append("\n".join(sub_buffer))
                text = "\n\n".join(text_buffer)

                if not text:
                    await send_msg.send_prompt("Warning: No Model Data")
                await send_msg.send_render(text)
        else:
            await send_msg.send_response_check_code(response)