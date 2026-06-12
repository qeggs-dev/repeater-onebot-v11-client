from ...assist import PersonaInfo, SendMsg
from ...clients import ChatClient, DataRoutingField, CrossUserDataRouting
from ...command_register import CommandCaller
from .._bases import BaseChat

@CommandCaller.register
class Reference(BaseChat):
    cmd = "reference"
    aliases = {
        "ref",
        "REF",
        "Reference",
        "REFERENCE"
    }
    documents = f"""
        References the Context of other members to generate text
        Note: You Need to ensure that you and the other party, as well as the server, all allow cross-user data access.
        
        Usage:
        ```
        /{cmd} @somebody text
        ```
    """
    
    async def send_message(
        self,
        client: ChatClient,
        images: list[str],
        audios: list[str],
        videos: list[str],
        message: str,
        persona_info: PersonaInfo,
        send_msg: SendMsg
    ) -> str:
        if not persona_info.noself_at_list:
            await send_msg.send_error("Please at a member to get reference.")
            
        response = await client.send_message(
            message = message,
            cross_user_data_routing = CrossUserDataRouting(
                context = DataRoutingField(
                    load_from_user_id = persona_info.noself_at_list[0]
                )
            ),
            image_url = images
        )

        return response