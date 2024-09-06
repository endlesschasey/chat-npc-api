from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Setting:
    host: str = "192.168.30.144"
    port: int = 8800
    AUDIO_URL: str = "http://192.168.30.144:5470/add_task"
    AUDIO_TASK_URL: str = "http://192.168.30.144:5570/get_task_info/"
    AUDIO_SECRET_KEY: str = "d1d2c0efba0959622de7e128b7e7a072f02ae7443ef3148d1d28b40af27e5316"