from pydantic import BaseModel, Field
import uuid
from app.utils.ollama_client import generate_response
from typing import List, Dict

class NPC(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    personality: str

    def respond_to_message(self, message: str, conversation_history: List[Dict[str, str]] = []) -> str:
        system_message = f"""你是一个名叫{self.name}的NPC。
        你的描述：{self.description}
        你的性格：{self.personality}
        请始终以你的身份回答用户的消息。"""
        
        messages = [
            {"role": "system", "content": system_message},
        ] + conversation_history + [
            {"role": "user", "content": message}
        ]
        
        response = generate_response(messages)
        return response.strip()

class NPCResponse(BaseModel):
    message: str

class NPCManager:
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

    def add_npc(self, npc: NPC):
        print(f"Adding NPC: {npc}")  # 添加这行来调试
        if npc.id in self.npcs:
            print(f"Warning: Overwriting existing NPC with id {npc.id}")
        self.npcs[npc.id] = npc
        print(f"NPCs after adding: {self.npcs}")  # 添加这行来调试

    def get_npc(self, npc_id: str) -> NPC:
        return self.npcs.get(npc_id)

    def get_npc_list(self) -> List[Dict[str, str]]:
        npc_list = [{"id": npc.id, "name": npc.name} for npc in self.npcs.values()]
        print(f"Getting NPC list: {npc_list}")
        return npc_list

    def start_conversation(self, npc_id: str) -> str:
        if npc_id not in self.conversations:
            self.conversations[npc_id] = []
        return npc_id

    def send_message(self, npc_id: str, message: str) -> str:
        npc = self.get_npc(npc_id)
        if not npc:
            raise ValueError("NPC not found")

        conversation = self.conversations.get(npc_id, [])
        response = npc.respond_to_message(message, conversation)

        conversation.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ])
        self.conversations[npc_id] = conversation

        return response

    def get_conversation_history(self, npc_id: str) -> List[Dict[str, str]]:
        return self.conversations.get(npc_id, [])
