import ollama
OLLAMA_HOST = "http://localhost:11434"

client = ollama.Client(host=OLLAMA_HOST)

response = client.chat(
    model="llama3",
    messages=[
        {"role": "user", "content": "你好，世界"}
    ]
)

print(response)
