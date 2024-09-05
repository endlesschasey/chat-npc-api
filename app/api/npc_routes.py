from fastapi import APIRouter, HTTPException, Body
from app.models.npc import NPC, NPCManager, NPCResponse
from typing import List, Dict

router = APIRouter()
npc_manager = NPCManager()

@router.post("/npcs", response_model=NPC)
async def create_npc(npc: NPC):
    npc_manager.add_npc(npc)
    return npc

@router.get("/npcs", response_model=List[Dict[str, str]])
async def get_npc_list():
    return npc_manager.get_npc_list()

@router.post("/conversations/{npc_id}", response_model=NPCResponse)
async def send_message(npc_id: str, message: str = Body(..., embed=True)):
    try:
        response = npc_manager.send_message(npc_id, message)
        return NPCResponse(message=response)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/conversations/{npc_id}", response_model=List[Dict[str, str]])
async def get_conversation_history(npc_id: str):
    history = npc_manager.get_conversation_history(npc_id)
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return history