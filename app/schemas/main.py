from typing import List, Tuple
from pydantic import BaseModel



class ChatRequest(BaseModel):
    message: str
    history: List[Tuple[str, str]] = []
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0