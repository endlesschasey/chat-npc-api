import ollama
from ollama import Message

class Agent:
    def __init__(self, system_prompt: str) -> None:
        OLLAMA_HOST = "http://localhost:11434"
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.system_prompt = system_prompt

    async def chat(self, messages, model="qwen2"):
        try:
            if messages[0]['role'] != 'system':
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    *messages
                ]
            response = self.client.chat(
                model=model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
