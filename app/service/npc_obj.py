import uuid
from typing import Dict, List, Optional, Tuple
from app.utils.ollama_client import Agent
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
        self.agent = Agent(self._create_system_prompt())

    def _create_system_prompt(self) -> str:
        return f"""
        你是一个角色扮演机器人，你要扮演的角色名称为: {self.name},
        你的基本信息是{self.basic_info},
        你的性格是{self.personality}，
        你的目标和背景是{self.goal_and_background}，
        你的个人介绍是{self.personal_intro}，
        你的性格特征是{self.personality_traits}，
        你常用的台词有这些{self.lines}。
        """

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


