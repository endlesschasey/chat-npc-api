from fastapi import FastAPI
from app.api import npc_routes

app = FastAPI()

app.include_router(npc_routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the NPC Chat System"}