from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Setting:
    host: str = "192.168.30.144"
    port: int = 8800