import time
import asyncio
from typing import Awaitable

class LimitSpeed:
    def __init__(
            self,
            limit_speed_per_minute: int | float | None = 100
        ):
        self.limit_speed_per_minute = limit_speed_per_minute
        self.last_send_time = time.monotonic_ns()
    
    async def submit(self, task: Awaitable) -> None:
        if self.limit_speed_per_minute is not None:
            current_time = time.monotonic_ns()
            last_time_dalta = current_time - self.last_send_time
            expected_time_delta = self.limit_speed_per_minute / 60
            time_dalta = max(0, expected_time_delta - (last_time_dalta / 1e9))
            if time_dalta > 0:
                await asyncio.sleep(time_dalta)
        await task