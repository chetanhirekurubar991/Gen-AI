import ollama

# Test connection
response = ollama.chat(
    model='qwen3:4b',
    messages=[
        {'role': 'user', 'content': 'Say hello in one sentence'}
    ]
)

print(response['message']['content'])