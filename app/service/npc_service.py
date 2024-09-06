import os
import uuid
import asyncio
from typing import Dict, List
from app.models.npc import *
from app.utils.parse_info import parse_npc_file
from app.service.npc_obj import NPC

class NPCService:
    # 单例模式
    _instance = None
    _initialized = False 

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NPCService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.npcs: Dict[str, NPC] = {}
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.load_npcs_from_files()
        self._initialized = True

    def load_npcs_from_files(self, folder_path: str = "npcs"):
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(folder_path, filename)
                npc_data = parse_npc_file(file_path)
                npc = NPC(
                    role_id=npc_data["basic_info"].get("角色ID"),
                    name=npc_data["basic_info"].get("名字"),
                    description=npc_data["basic_info"].get("印象描述"),
                    personality=npc_data["basic_info"].get("性格简述"),
                    lines=npc_data["lines"],
                    goal_and_background=npc_data["goal_and_background"],
                    personal_intro=npc_data["personal_intro"],
                    personality_traits=npc_data["personality_traits"],
                    basic_info=npc_data["basic_info"]
                )
                self.npcs[npc.name] = npc

    def get_npc(self, name: str) -> NPC:
        return self.npcs.get(name)

    def get_npc_list(self) -> List[Dict[str, str]]:
        return [npc for npc in self.npcs.keys()]
    
    async def send_message(self, message: NPCMessage) -> NPCResponse:
        npc = self.get_npc(message.name)
        if not npc:
            raise ValueError("NPC不存在")

        response, conversation_id = await npc.add_message(message.conversation_id, message.message)

        # 提交一个线程，将NPC的对话生成音频
        if message.if_audio:
            audio_id = str(uuid.uuid4())
            asyncio.create_task(npc.generate_audio(response, audio_id))  

        return NPCResponse(message=response, conversation_id=conversation_id, audio_id=audio_id)

    async def get_npc_audio(self, request: AudioRequest) -> str:
        npc = self.get_npc(request.name)
        if not npc:
            raise ValueError("NPC不存在")
        return await npc.get_audio_url(request.audio_id)

    async def audio_callback(self, callback: AudioCallback):
        npc = self.get_npc(callback.name)
        if not npc:
            raise ValueError("NPC不存在")
        await npc.audio_callback(callback.audio_id, callback.status, callback.url)

npc_service = NPCService()
