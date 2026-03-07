import asyncio
import aiohttp
async def ask_ollama(model,prompt):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "http://localhost:11434/api/generate",
                json={
                    "model":model,
                    "prompt":prompt,
                    "stream":False
                },
            ) as response:
                print(f"{model}: Thinking...")
                data=await response.json()
                return data["response"]
        except Exception as e:
            print(e)
async def main():
    result=await ask_ollama("qwen3:4b","About Qwen Models")
    print(result)
asyncio.run(main())
