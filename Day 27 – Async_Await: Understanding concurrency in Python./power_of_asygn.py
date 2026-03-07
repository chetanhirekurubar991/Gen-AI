import asyncio
import time
import aiohttp
async def ask_ollama(prompt,model):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11434/api/generate",
            json={
                "model":model,
                "prompt":prompt,
                "stream":False
            }
        ) as response:
            data=await response.json()
            return data
async def compare_models(prompt):
    before=time.time()
    results=await asyncio.gather(
        ask_ollama(prompt,"qwen3:4b"),
        ask_ollama(prompt,"deepseek-coder:6.7b")
    )
    after=time.time()
    total_time=after-before
    for result in results:
        print(f"{result["model"]} : ")
        print(f"{result["response"]}")
    print()
    print(f"Total time taken is : {total_time:.2f}")
async def main():
        await compare_models("Explain async/await in one sentence")
asyncio.run(main())