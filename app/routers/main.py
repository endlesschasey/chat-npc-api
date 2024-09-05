from fastapi import APIRouter

from config.settings import Setting
from app.schemas.main import ChatRequest
router = APIRouter()

@router.post("/")
async def main():
    return {"message": "Hello World"}

@router.post("/chat")
async def chat(request: ChatRequest):
    pass
