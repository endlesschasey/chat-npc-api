import uuid
import hashlib
import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.utils.agent import Agent
from config.settings import Setting
from loguru import logger

class NPC:
    def __init__(self, role_id: str, name: str, description: str, personality: str, lines: List[str], goal_and_background: str, personal_intro: str, personality_traits: Dict[str, str], basic_info: Dict[str, str]):
        self.name = name # 名字
        self.description = description # 描述
        self.personality = personality # 性格
        self.role_id = role_id # 音频生成:角色ID

        # 完整内容
        self.lines = lines # 对话
        self.goal_and_background = goal_and_background # 目标和背景
        self.personal_intro = personal_intro # 个人介绍
        self.personality_traits = personality_traits # 性格特征
        self.basic_info = basic_info # 基本信息

        # 对话历史
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
        self.audio_history: Dict[str, Tuple[str, str]] = {}
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
        请你根据这些信息进行角色扮演。
        要求：
        1. 尽量简洁地回答，只回答明确提到或询问的内容，最好不超过 20 个字。
        2. 假设用户知道您是谁；除非特别询问，否则不要自我介绍。
        3. 确保您的回答符合角色的既定特征和背景。
        4. 与正在进行的对话及其上下文保持一致。
        5. 调整您的回答以适应当前的对话场景。
        6. 适当时，请随意逐字使用提供的台词。
        7. 力求自然的对话模式，避免过度做作的言语。
        8. 您必须使用与用户相同的语言进行回复。
        9. 您需要在回答的最后带上两个心情词，格式为(b:身体心情词+f:脸部心情词)，例如 "我们今天去哪里？(b:开心+f:微笑)"
        10. 心情词只能在下列词库中选择:
            身体：放松,认真,思索,开心,害羞,惊讶
            脸部：放松,认真,思索,微笑,沮丧,嫌弃
        """

    async def add_message(self, conversation_id: Optional[str] = None, message: Optional[str] = None) -> Tuple[str, str]:
        if conversation_id is None or conversation_id == "":
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

    async def generate_audio(self, message: str, audio_id: str):
        try:
            token = "npc_audio_generate"
            timestamp = int(datetime.now().timestamp())
            data = {
                "role_id": self.role_id,
                "text": message,
                "text_language": "中文",
                "timestamp": timestamp,
                "token": token,
                "sign": self._generate_sign(token, timestamp, Setting.AUDIO_SECRET_KEY).upper(),
                "callback_url": f"http://{Setting.host}:{Setting.port}/npc/audio/callback",
                "proxy_data": {
                    "audio_id": audio_id,
                    "name": self.name
                }
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(Setting.AUDIO_URL, json=data) as response:
                    if response.status == 200:
                        response = await response.json()
                        logger.info(f"Generate audio: {response.get('status')}")
                        self.audio_history[audio_id] = (response.get("task_id"), None)
                    else:
                        raise Exception(f"Failed to generate audio: {response.status}")
        except Exception as e:
            raise e

    async def audio_callback(self, audio_id: str, status: str, url: Optional[str] = None):
        if status == "success":
            task_id, _ = self.audio_history.get(audio_id, (None, None))
            self.audio_history[audio_id] = (task_id, url, status)
        else:
            self.audio_history[audio_id] = (None, None, status)
            logger.error(f"Failed to generate audio: {status}")

    async def get_audio_url(self, audio_id: str) -> str:
        try:
            task_id, url, status = self.audio_history.get(audio_id, (None, None, None))
            if status == "success" and url:
                return url
            elif status == "success" and not url:
                if task_id:
                        # 等待10秒，看是否有回调
                        for _ in range(10):
                            await asyncio.sleep(1)
                            _, _, url = self.audio_history.get(audio_id, (None, None, None))
                            if url:
                                return url

                        # 如果10秒后仍然没有url，则调用接口
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"{Setting.AUDIO_TASK_URL}{task_id}") as response:
                                if response.status == 200:
                                    response_data = await response.json()
                                    url = response_data.get("url")
                                    if url:
                                        # 更新audio_history
                                        self.audio_history[audio_id] = (task_id, url)
                                        return url
                                    else:
                                        raise Exception(f"Audio URL not found for task ID {task_id}")
                                else:
                                    raise Exception(f"Failed to get audio: {response.status}")
                else:
                    raise Exception(f"Audio ID {audio_id} not found")
            else:
                raise Exception(f"Audio ID {audio_id} failed")
        except Exception as e:
            logger.error(f"Failed to get audio: {e}")
            return None

    def _generate_sign(self, token: str, timestamp: int, secret_key: str) -> str:
        sign_str = f"{timestamp}{token}{secret_key}"
        return hashlib.sha256(sign_str.encode()).hexdigest()


