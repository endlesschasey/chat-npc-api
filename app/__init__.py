from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import *

def create_app():
    app = FastAPI(
        title="NPC智能对话API服务",
        description="提供NPC的定制和对话功能的API服务",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(main_router, prefix="/api", tags=["main"])
    app.include_router(npc_router, prefix="/npc", tags=["npc"])  # 新增NPC路由

    return app

app = create_app()