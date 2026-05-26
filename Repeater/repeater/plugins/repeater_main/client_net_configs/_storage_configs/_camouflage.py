from pydantic import BaseModel
class Camouflage(BaseModel):
    send_msg_limit_speed_per_minute: int | float | None = 100