import os
from typing import Dict, List
from app.models.npc import NPCMessage, NPCResponse
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

    def start_conversation(self, npc_id: str) -> str:
        if npc_id not in self.conversations:
            self.conversations[npc_id] = []
        return npc_id

    async def send_message(self, message: NPCMessage) -> NPCResponse:
        npc = self.get_npc(message.name)
        if not npc:
            raise ValueError("NPC不存在")

        response = await npc.add_message(message.conversation_id, message.message)

        return response

    def get_conversation_history(self, npc_id: str) -> List[Dict[str, str]]:
        return self.conversations.get(npc_id, [])

npc_service = NPCService()
