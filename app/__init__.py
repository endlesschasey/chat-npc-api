from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from app.routers import *
import os

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
    
    # 挂载 Next.js 静态文件
    app.mount("/_next", StaticFiles(directory="frontend/.next"), name="static")
    
    app.include_router(main_router, prefix="/api", tags=["main"])
    app.include_router(npc_router, prefix="/npc", tags=["npc"])
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path == "":
            full_path = "index.html"
        
        # 尝试从 .next/server/pages 目录提供文件
        server_pages_path = os.path.join("frontend", ".next", "server", "pages", full_path)
        if os.path.isfile(server_pages_path):
            return FileResponse(server_pages_path)
        
        # 如果不是文件，尝试提供 index.html
        index_html = os.path.join("frontend", ".next", "server", "pages", "index.html")
        if os.path.isfile(index_html):
            return FileResponse(index_html)
        
        # 如果 index.html 不存在，尝试提供 _app.js
        app_js = os.path.join("frontend", ".next", "server", "pages", "_app.js")
        if os.path.isfile(app_js):
            return FileResponse(app_js)
        
        # 如果都不存在，返回 404
        return HTMLResponse("<h1>404 Not Found</h1>")
    
    return app

app = create_app()