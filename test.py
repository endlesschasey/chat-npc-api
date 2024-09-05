import ollama

client = ollama.Client(host="http://localhost:11434")

response = client.chat(
    model="qwen2:1.5b",
    messages=[
        {"role": "user", "content": "你好，世界"}
    ]
)

print(response)
