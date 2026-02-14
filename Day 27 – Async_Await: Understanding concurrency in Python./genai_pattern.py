import asyncio
import time
import aiohttp


async def ask_ollama(session, prompt, model):
    async with session.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
    ) as response:
        data = await response.json()
        return data["response"]


async def smart_llm_call(prompt, timeout=15):
    errors = []
    start_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        # Try qwen2.5:4b first
        try:
            # TODO: Add timeout logic here
            result=await asyncio.wait_for(ask_ollama(session,prompt,"qwen3:4b"),timeout)
            return {
                "success": True,
                "model_used": "qwen3:4b",
                "response": result,
                "time_taken": time.perf_counter() - start_time,
                "errors": errors
            }
        except asyncio.TimeoutError:
            # TODO: Log timeout and try fallback
            errors.append("qwen3:4b : TimeOut")
            print("Qwen AI model is timeout ,using fallback")
        except Exception as e:
            # TODO: Log error and try fallback
            errors.append(str(e))
            print(f"Error : {e}")

        try:
            result=await asyncio.wait_for(ask_ollama(session,prompt,"deepseek-coder:6.7b"),timeout)
            return {
                "success": True,
                "model_used": "deepseek-coder:6.7b",
                "response": result,
                "time_taken": time.perf_counter() - start_time,
                "errors": errors
            }
        except asyncio.TimeoutError:
            errors.append("deepseek-coder:6.7b : TimeOut")
            print("Both models time out")
        except Exception as e:
            errors.append(str(e))
            print(f"Error : {e}")

    # If we reach here, both failed

    return {
        "success": False,
        "model_used": None,
        "response": None,
        "time_taken": time.perf_counter() - start_time,
        "errors": errors
    }


async def main():
    # Test normal case
    result = await smart_llm_call("What is async?", timeout=30)
    print(result)
    print()
    print(f"Model : {result["model_used"]}")
    print(f"Answer : {result["response"]}")


asyncio.run(main())