from pydantic import BaseModel, Field, field_validator
from typing import Literal
from ._camouflage import Camouflage
from ._text_length_score_configs import TextLengthScoreConfigs
from ._server_api_timeout import ServerAPITimeout
from .._useless_button_words import useless_button_words
from ._behavioral_act import BehavioralACT

class StorageConfigs(BaseModel):
    text_length_score_configs: TextLengthScoreConfigs = Field(default_factory = TextLengthScoreConfigs)
    hello_content: str = "Repeater Is Ready!"
    hello_messages_by_weekday: dict[int | str, str] = Field(default_factory=dict, max_length=7)
    hello_messages_for_date: dict[str, str] = Field(default_factory=dict)
    behavioral_acts: dict[int | str, BehavioralACT] = Field(default_factory=dict)
    default_behavioral_act: BehavioralACT = Field(default_factory=BehavioralACT)
    backends: dict[str, str] = Field(default_factory=dict)
    default_backend: str = ""
    client_pool_size: int = Field(default=10, ge=1)
    usage_group_context: bool = False
    server_api_timeout:ServerAPITimeout = Field(default_factory = ServerAPITimeout)
    use_base64_image_url: bool = False
    camouflage: Camouflage = Field(default_factory = Camouflage)
    download_image_timeout: float = 600.0
    summarize_and_contract_default_message: str = "System Message: please sum up all the contents above."
    ciallo_content: str = "Ciallo~ (∠・ω< )⌒★"
    branch_file_size_use_abbreviation: bool = True
    hash_user_id: bool = False
    allow_send_any_message: bool = False
    model_first_chunk_timeout: int | float | None = 90.0
    max_reply_chain_length: int = 5
    max_text_file_size: int | None = None
    text_file_encoding: str = "utf-8"
    log_registed_handler_name: bool = True
    platform_interface_cache: bool = True
    platform_interface_cache_size: int | float = 1000
    platform_interface_cache_timeout: int | float = 60
    useless_button_words: list[str] = Field(default_factory=lambda: useless_button_words)
    useless_button_missing: str = "The button buzzed away."

    def __post_init__(self):
        self.behavioral_acts = {int(key): value for key, value in self.behavioral_acts.items()}
    
    def get_behavioral_act(self, user_id: int) -> BehavioralACT:
        if user_id in self.behavioral_acts:
            return self.behavioral_acts[user_id]
        else:
            return self.default_behavioral_act