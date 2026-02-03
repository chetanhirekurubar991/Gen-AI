import ollama
conversation = []
MAX_MESSAGES = 10
print('type quit to "exit",or "reset" to clean memory')
print("-"*60)
def add_to_memory():
    while True:
        user_prompt=input("Ask Anything...\n").strip()
        if not user_prompt:
            print("Don't leave..Ask anything..")
            continue
        elif user_prompt.lower() in ["quit"]:
            print("successfully quited..")
            break
        elif user_prompt.lower() == "reset":
            print("memory is cleaned start free chat")
            conversation.clear()
            continue
        elif user_prompt.lower() == "my memory":
            print(conversation)
            continue
        else:
            try:
                conversation.append({"role":"user","content":user_prompt})
                del conversation[:-MAX_MESSAGES]
                response=ollama.chat(
                    model="qwen3:4b",
                    messages=conversation,
                    options={"temperature":0.3,"num_ctx":2048})
                result=response["message"]["content"]
                conversation.append({"role":"assistant","content":result})
                print(result)
            except Exception as e:
                print(f'{e}')
if __name__=="__main__":
    add_to_memory()