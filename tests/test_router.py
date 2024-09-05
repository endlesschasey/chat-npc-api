import sys
import os

# 获取项目根目录的路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将项目根目录添加到 Python 路径中
sys.path.insert(0, project_root)

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.npc import NPC, NPCManager
from app.api.npc_routes import npc_manager

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_npc_manager():
    npc_manager.npcs.clear()
    npc_manager.conversations.clear()

def test_create_npc():
    npc_data = {
        "name": "张三",
        "description": "一个友好的村民",
        "personality": "热情、乐于助人"
    }
    response = client.post("/api/npcs", json=npc_data)
    assert response.status_code == 200
    npc = response.json()
    assert npc["name"] == npc_data["name"]
    assert npc["description"] == npc_data["description"]
    assert npc["personality"] == npc_data["personality"]
    assert "id" in npc

def test_get_npc_list():
    # 清空 npc_manager
    npc_manager.npcs.clear()
    print("NPCs after clear:", npc_manager.npcs)

    # 创建两个NPC
    npc1 = NPC(name="张三", description="村民1", personality="友好")
    npc2 = NPC(name="李四", description="村民2", personality="严肃")
    
    print("NPC1:", npc1)
    print("NPC2:", npc2)
    
    npc_manager.add_npc(npc1)
    print("NPCs after adding npc1:", npc_manager.npcs)
    
    npc_manager.add_npc(npc2)
    print("NPCs after adding npc2:", npc_manager.npcs)

    # 打印 npc_manager 中的 NPC
    print("Final NPCs in manager:", npc_manager.npcs)

    response = client.get("/api/npcs")
    assert response.status_code == 200
    npc_list = response.json()
    
    # 打印响应的 NPC 列表
    print("NPC list from response:", npc_list)

    assert len(npc_list) == 2, f"Expected 2 NPCs, but got {len(npc_list)}"
    assert {"id": npc1.id, "name": npc1.name} in npc_list
    assert {"id": npc2.id, "name": npc2.name} in npc_list

def test_send_message():
    npc = NPC(name="张三", description="村民", personality="友好")
    npc_manager.add_npc(npc)

    message = "你好,能介绍一下这个村子吗?"
    response = client.post(f"/api/conversations/{npc.id}", json={"message": message})
    assert response.status_code == 200
    npc_response = response.json()
    assert "message" in npc_response
    assert len(npc_response["message"]) > 0

def test_send_message_to_nonexistent_npc():
    nonexistent_id = "nonexistent_id"
    message = "你好"
    response = client.post(f"/api/conversations/{nonexistent_id}", json={"message": message})
    assert response.status_code == 404
    assert response.json()["detail"] == "NPC not found"

def test_get_conversation_history():
    npc = NPC(name="张三", description="村民", personality="友好")
    npc_manager.add_npc(npc)

    # 发送两条消息
    client.post(f"/api/conversations/{npc.id}", json={"message": "你好"})
    client.post(f"/api/conversations/{npc.id}", json={"message": "这个村子怎么样?"})

    response = client.get(f"/api/conversations/{npc.id}")
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 4  # 两个用户消息和两个NPC回复
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[2]["role"] == "user"
    assert history[3]["role"] == "assistant"

def test_get_conversation_history_nonexistent_npc():
    nonexistent_id = "nonexistent_id"
    response = client.get(f"/api/conversations/{nonexistent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"