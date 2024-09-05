from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.models.npc import NPC, NPCResponse

router = APIRouter()

npcs = {}  # 用于存储NPC实例的字典

class NPCCreate(BaseModel):
    name: str
    description: str
    personality: str

class NPCMessage(BaseModel):
    message: str

@router.post("/create", response_model=NPC)
async def create_npc(npc: NPCCreate):
    new_npc = NPC(name=npc.name, description=npc.description, personality=npc.personality)
    npcs[new_npc.id] = new_npc
    return new_npc

@router.get("/list", response_model=List[NPC])
async def list_npcs():
    return list(npcs.values())

@router.post("/{npc_id}/chat", response_model=NPCResponse)
async def chat_with_npc(npc_id: str, message: NPCMessage):
    if npc_id not in npcs:
        raise HTTPException(status_code=404, detail="NPC不存在")
    npc = npcs[npc_id]
    response = npc.respond_to_message(message.message)
    return NPCResponse(message=response)