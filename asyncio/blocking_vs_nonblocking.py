import asyncio
import time

async def quick_task():
    """A task that prints a message every 0.5 seconds."""
    for i in range(3):
        print(f"   ⚡️ Quick task is running... ({i+1}/3)")
        await asyncio.sleep(0.5)

async def bad_blocking_task():
    print("🔴 BAD task started. I am about to FREEZE the entire program for 2s.")
    # CRITICAL MISTAKE: This blocks the CPU. Nothing else can run.
    time.sleep(2) 
    print("🔴 BAD task finished.")

async def good_async_task():
    print("🟢 GOOD task started. I will pause for 2s, but let you keep working.")
    # CORRECT: This pauses this specific function, but lets the loop run other things.
    await asyncio.sleep(2)
    print("🟢 GOOD task finished.")

async def main():
    print("--- SCENARIO 1: The Bad Way (Blocking) ---")
    print("Notice how the Quick Task CANNOT run until the Bad Task is done.")
    # We try to run them together, but time.sleep() prevents it.
    await asyncio.gather(bad_blocking_task(), quick_task())
    
    print("\n" + "="*40 + "\n")

    print("--- SCENARIO 2: The Good Way (Non-blocking) ---")
    print("Notice how the Quick Task runs WHILE the Good Task is waiting.")
    await asyncio.gather(good_async_task(), quick_task())

if __name__ == "__main__":
    asyncio.run(main())
