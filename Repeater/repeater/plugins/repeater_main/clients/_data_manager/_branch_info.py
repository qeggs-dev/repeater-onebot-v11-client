from pydantic import BaseModel
from datetime import datetime
from ...assist import format_carry_duration
from ...client_net_configs import storage_configs

SIZE_UNITS = [
    ("Bytes", "B", 1024),
    ("Kibibyte", "KiB", 1024),
    ("Mebibyte", "MiB", 1024),
    ("Gibibyte", "GiB", 1024),
    ("Tebibyte", "TiB", 1024),
    ("Pebibyte", "PiB", 1024),
    ("Exbibyte", "EiB", 1024),
]

FINAL_SIZE_UNIT = ("Yobibyte", "YiB")

class BranchInfo(BaseModel):
    """Branch Info"""
    branch_id: str = ""
    size: int = 0
    modified_time: float = 0
    file_exists: bool = False

    def modified_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.modified_time)
    
    @property
    def readable_size(self) -> str:
        return format_carry_duration(
            self.size,
            SIZE_UNITS,
            final_level = FINAL_SIZE_UNIT,
            use_abbreviation = storage_configs.branch_file_size_use_abbreviation
        )
