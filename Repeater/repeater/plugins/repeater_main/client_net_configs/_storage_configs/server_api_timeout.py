from pydantic import BaseModel

class ServerAPITimeout(BaseModel):
    chat: float = 600.0
    context: float = 10.0
    prompt: float = 10.0
    config: float = 10.0
    data_manager: float = 10.0
    licenses: float = 10.0
    model_info: float = 1200.0
    status: float = 10.0
    version: float = 10.0
    request_log: float = 1200.0
    variable_expansion: float = 40.0
    render: float = 600.0