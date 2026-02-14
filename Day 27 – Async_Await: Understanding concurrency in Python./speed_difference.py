import asyncio
import time
import aiohttp


async def ask_ollama(prompt, model):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
        ) as response:
            data = await response.json()
            return {"model": model, "response": data["response"]}


async def sequential_version(prompt):
    # TODO: Call models one after another (await first, then await second)
    # Time it and return total_time
    before=time.time()
    await ask_ollama(prompt, "qwen3:4b")
    await ask_ollama(prompt, "deepseek-coder:6.7b")
    after=time.time()
    return after-before


async def parallel_version(prompt):
    # TODO: Use asyncio.gather() to call both at once
    # Time it and return total_time
    before=time.time()
    result= await asyncio.gather(
        ask_ollama(prompt, "qwen3:4b"),
        ask_ollama(prompt, "deepseek-coder:6.7b")
    )
    after=time.time()
    return after-before

async def main():
    prompt = "What is Python?"
    # TODO: Run both versions and compare times
    sequential=await sequential_version(prompt)
    parallel=await parallel_version(prompt)
    # Print: "Sequential: X seconds, Parallel: Y seconds, Speedup: Zx"
    print(f"Sequential: {sequential:.2f} seconds, Parallel: {parallel:.2f} seconds, Speedup: {(sequential/parallel):.2f}")

asyncio.run(main())