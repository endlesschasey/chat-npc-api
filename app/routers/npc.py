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
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{npc_id}/history", response_model=List[dict])
async def get_chat_history(npc_id: str):
    return npc_service.get_conversation_history(npc_id)