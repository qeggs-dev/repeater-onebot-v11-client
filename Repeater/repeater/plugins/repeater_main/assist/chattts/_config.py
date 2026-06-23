import random

from pydantic import BaseModel, Field
from ...config_loader import Loader, Mode

class APIArgs(BaseModel):
    voice: str = ""
    speed: int = 6
    tts_prompt: str = "[break_6]"
    temperature: float = 0.2
    top_p: float = 0.7
    top_k: int = 20
    refine_max_new_token: int = 384
    infer_max_new_token: int = 2048
    text_seed: int = Field(default_factory=lambda: random.randint(0, 2**32 - 1))
    skip_refine: bool = True
    is_stream: bool = False
    custom_voice: int = 0
    

class TTSConfig(BaseModel):
    base_url: str = "http://127.0.0.1:8123"
    api_args: APIArgs = Field(default_factory=APIArgs)
    timeout: float = 60.0

loader: Loader[TTSConfig] = Loader(
    model = TTSConfig,
    path = "configs/tts.json",
    mode = Mode.JSON
)

tts_config: TTSConfig = loader.load(unexist_create = True)