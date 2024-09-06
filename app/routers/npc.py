from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.models.npc import *
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

@router.post("/audio", response_model=AudioResponse)
async def get_npc_audio(request: AudioRequest):
    url = await npc_service.get_npc_audio(request)
    return AudioResponse(url=url)

@router.post("/audio/callback", include_in_schema=False)
async def audio_callback(callback: AudioCallback):
    await npc_service.audio_callback(callback)


