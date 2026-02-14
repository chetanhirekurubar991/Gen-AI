import asyncio
import time
async def simulate_llm_call(model_name, delay):
    print(f"{model_name}: Calling...")
    await asyncio.sleep(delay)
    print(f"{model_name} result")


def simulate_llm_call_sync(model_name, delay):
    print(f"{model_name}: Calling...")
    time.sleep(delay)
    print(f"{model_name} result")


def sync_version():
    before=time.time()
    simulate_llm_call_sync("OpenAI",2)
    simulate_llm_call_sync('Anthropic',3)
    simulate_llm_call_sync('Gemini',2)
    after=time.time()
    total_time=after-before
    return total_time
async def async_version():
    before=time.time()
    result=await asyncio.gather(
        simulate_llm_call("OpenAI", 2),
        simulate_llm_call('Anthropic', 3),
        simulate_llm_call('Gemini', 2)
    )
    after=time.time()
    total_time=after-before
    return total_time
async def main():
    print("Synchronous Calling")
    sync_time=sync_version()
    print()
    print("Asynchronous Calling")
    async_time=await async_version()
    print(f"Sync took {sync_time:.2f} seconds and Async took {async_time:.2f}")
    print(f"Async is {(sync_time/async_time):.2f}x faster!")
asyncio.run(main())