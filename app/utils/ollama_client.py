import ollama

OLLAMA_HOST = "http://localhost:11434"
client = ollama.Client(host=OLLAMA_HOST)

def generate_response(messages, model="qwen2:7b"):
    try:
        response = client.chat(
            model=model,
            messages=messages
        )
        return response['message']['content']
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
