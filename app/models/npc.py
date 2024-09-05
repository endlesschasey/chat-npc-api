from pydantic import BaseModel, Field
import uuid
from typing import List, Dict, Optional

class NPCMessage(BaseModel):
    name: str = Field(default=..., description="NPC名字")
    message: str = Field(default=..., description="NPC消息")
    conversation_id: Optional[str] = Field(default=None, description="对话ID(第一次对话时没有 ID, 后续对话时需要传入)")

class NPCResponse(BaseModel):
    message: str = Field(default=..., description="NPC回复") 
    conversation_id: str = Field(default=..., description="对话ID")
