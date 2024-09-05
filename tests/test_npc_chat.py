import pytest
from fastapi.testclient import TestClient
from app import app
from app.models.npc import NPCMessage, NPCResponse

client = TestClient(app)

def test_multi_turn_chat():
    conversation_id = None

    # 第一轮对话：介绍自己
    response = client.post("/npc/chat", json={
        "name": "天狐恋",
        "message": "你好,我是李大钊",
        "conversation_id": conversation_id
    })
    print(response.json()["message"])
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data
    conversation_id = data["conversation_id"]

    # 第二轮对话：询问 NPC 是否记得用户的名字
    response = client.post("/npc/chat", json={
        "name": "天狐恋",
        "message": "你还记得我的名字吗?",
        "conversation_id": conversation_id
    })
    print(response.json()["message"])
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data
    assert data["conversation_id"] == conversation_id
    assert "李大钊" in data["message"]

    # 第三轮对话：继续对话以确保连贯性
    response = client.post("/npc/chat", json={
        "name": "天狐恋",
        "message": "村子里有什么特产吗?",
        "conversation_id": conversation_id
    })
    print(response.json()["message"])
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "conversation_id" in data
    assert data["conversation_id"] == conversation_id
