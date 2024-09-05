from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.npc import NPCMessage, NPCResponse
from app.service.npc_service import npc_service

router = APIRouter()

@router.get("/list", response_model=List[str])
async def list_npcs():
    return npc_service.get_npc_list()

@router.post("/chat", response_model=NPCResponse)
async def chat_with_npc(message: NPCMessage):
    try:
        response = await npc_service.send_message(message)
        return NPCResponse(message=response[0], conversation_id=response[1])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
