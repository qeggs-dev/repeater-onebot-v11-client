from pydantic import BaseModel
from ....client_net_configs import HelloContent

class UserConfigs(BaseModel):
    backend: str | None = None
    hello_content: HelloContent | None = None