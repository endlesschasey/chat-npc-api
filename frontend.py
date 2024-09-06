import streamlit as st
import requests
import json
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://192.168.30.144:8800/npc"

def get_npc_list():
    response = requests.get(f"{API_URL}/list")
    return response.json()

def send_message(name, message, conversation_id=None, if_audio=True):
    data = {
        "name": name,
        "message": message,
        "conversation_id": conversation_id,
        "if_audio": if_audio
    }
    response = requests.post(f"{API_URL}/chat", json=data)
    return response.json()

def get_audio_url(name, audio_id):
    data = {
        "name": name,
        "audio_id": audio_id
    }
    try:
        response = requests.post(f"{API_URL}/audio", json=data)
        response.raise_for_status()  # 如果状态码不是200，将引发HTTPError异常
        logger.info(f"Audio API response status: {response.status_code}")
        logger.info(f"Audio API response content: {response.text}")
        
        if response.text and response.text.lower() != 'null':
            json_response = response.json()
            if isinstance(json_response, dict):
                return json_response.get("url")
            elif isinstance(json_response, str):
                return json_response
        logger.warning("Empty or null response from audio API")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching audio URL: {str(e)}")
        return None

st.title("NPC聊天系统")

# NPC列表和选择部分
st.header("选择NPC进行对话")
npc_list = get_npc_list()
selected_npc = st.selectbox("选择NPC", options=npc_list)

# 对话部分
st.header(f"与 {selected_npc} 对话")

# 使用session_state来保存对话历史和conversation_id
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = None

user_message = st.text_input("输入你的消息")
if st.button("发送"):
    if user_message:
        # 添加用户消息到历史
        st.session_state.conversation_history.append({"role": "user", "content": user_message})
        
        # 发送消息给NPC
        response = send_message(selected_npc, user_message, st.session_state.conversation_id, if_audio=True)
        
        # 更新conversation_id
        st.session_state.conversation_id = response["conversation_id"]
        
        # 添加NPC回复到历史
        st.session_state.conversation_history.append({
            "role": "assistant", 
            "content": response["message"],
            "audio_id": response.get("audio_id")
        })
        
        # 清空输入框并重新运行
        st.rerun()

# 显示对话历史
st.header("对话历史")
for idx, message in enumerate(st.session_state.conversation_history):
    if message["role"] == "user":
        st.text_input("你", message["content"], key=f"user_{idx}", disabled=True)
    else:
        st.text_area("NPC", message["content"], key=f"npc_{idx}", disabled=True)
        
        if "audio_id" in message:
            # 尝试获取音频URL
            audio_url = None
            time.sleep(5)
            for attempt in range(10):  # 尝试10次，每次间隔1秒
                audio_url = get_audio_url(selected_npc, message["audio_id"])
                if audio_url:
                    break
                logger.info(f"Attempt {attempt + 1}: Audio URL not ready, retrying...")
                time.sleep(1)
            
            if audio_url:
                st.audio(audio_url, format="audio/wav")
            else:
                st.warning("音频生成失败或尚未准备好")
                logger.warning(f"Failed to get audio URL after 10 attempts for audio_id: {message['audio_id']}")

st.button("清空对话历史", on_click=lambda: st.session_state.clear())