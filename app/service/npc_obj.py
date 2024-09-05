import uuid
from typing import Dict, List, Optional, Tuple
from utils.ollama_client import Agent
class NPC:
    def __init__(self, name: str, description: str, personality: str, lines: List[str], goal_and_background: str, personal_intro: str, personality_traits: Dict[str, str], basic_info: Dict[str, str]):
        self.name = name # 名字
        self.description = description # 描述
        self.personality = personality # 性格

        # 完整内容
        self.lines = lines # 对话
        self.goal_and_background = goal_and_background # 目标和背景
        self.personal_intro = personal_intro # 个人介绍
        self.personality_traits = personality_traits # 性格特征
        self.basic_info = basic_info # 基本信息

        # 对话历史
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
        # 对话实例
        self.agent = Agent()

    async def add_message(self, conversation_id: Optional[str] = None, message: Optional[str] = None) -> Tuple[str, str]:
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        self.conversation_history[conversation_id].append({
            "role": "user", 
            "content": message
        })
        response = await self.agent.chat(self.conversation_history[conversation_id])
        self.conversation_history[conversation_id].append({
            "role": "assistant",
            "content": response
        })
        return response, conversation_id


