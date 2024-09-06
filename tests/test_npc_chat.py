import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app import app
from app.models.npc import NPCMessage, NPCResponse

client = TestClient(app)

def test_multi_turn_chat():
    conversation_id = None
    npc_name = "天狐恋"

    conversations = [
        "你好,我是旅行者, 请问你是谁呀？",
        "嘿天狐恋，你还记得我的名字吗? 请大声的说出来我的名字是什么？",
        "你有喜欢的人吗？或者偶像也可以？",
        "最近发生了什么事情吗？为什么会有黑衣人追着你？"
    ]

    for turn, user_message in enumerate(conversations):
        print(f"\n--- 对话轮次 {turn + 1} ---")
        print(f"用户: {user_message}")

        # 发送消息并请求音频
        response = client.post("/npc/chat", json={
            "name": npc_name,
            "message": user_message,
            "conversation_id": conversation_id,
            "if_audio": True
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "conversation_id" in data
        assert "audio_id" in data
        
        conversation_id = data["conversation_id"]
        print(f"NPC回复: {data['message']}")

        # 根据对话轮次进行特定的断言
        if turn == 0:
            assert npc_name in data["message"]
        elif turn == 1:
            assert "旅行者" in data["message"]
        elif turn == 2:
            assert "网络歌姬" in data["message"] or "偶像" in data["message"]
        elif turn == 3:
            assert "舞台的工作人员" in data["message"] or "黑衣人" in data["message"]

        # 请求音频URL
        now = datetime.now()
        audio_response = client.post("/npc/audio", json={
            "audio_id": data["audio_id"],
            "name": npc_name
        })
        return_time = datetime.now()
        print(f"请求音频接口耗时: {return_time - now}")
        
        assert audio_response.status_code == 200
        audio_data = audio_response.json()
        assert "url" in audio_data
        assert audio_data["url"].startswith("http")
        assert "yongye" in audio_data["url"]
        print(f"音频URL: {audio_data['url']}")

    print("\n测试完成：多轮对话和音频生成成功")