llm_stop = ["exit", "quit"]
def cli_chatbot():
    while True:
        try:
            user_input = input("Enter a Prompt: ").strip()
            if user_input.lower() in llm_stop:
                print("Quited Successfully! Come back Soon...")
                return
            elif not user_input:
                print("Don't leave! Ask anything...")
                continue
            else:
                print(f"Received your input: {user_input} \nAssistant: connecting to llm...")
        except KeyboardInterrupt:
            print(f"\n\n Quited! Come back soon!")
            return
        except Exception as e:
            print(f"{e}")

if __name__=="__main__":
    cli_chatbot()