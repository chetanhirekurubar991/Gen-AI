import ollama
conversation = []
MAX_MESSAGES = 10
print('type quit to "exit",or "reset" to clean memory')
print("-"*60)
def add_to_memory():
    while True:
        try:
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
                        model="deepseek-coder:6.7b",
                        messages=conversation,
                        )
                    result=response["message"]["content"]
                    conversation.append({"role":"assistant","content":result})
                    print(result)
                except KeyboardInterrupt:
                    print("Quited..")
                except Exception as e:
                    print(f'{e}')
        except KeyboardInterrupt:
            print("Error : KeyboardInterrupt its Quited")
            return
        except Exception as e:
            print(f"Error : {e}")
            return
if __name__=="__main__":
    add_to_memory()