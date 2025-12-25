import asyncio
import time

async def task(name,delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    completion_message = f"Task {name} completed after {delay}s"
    print(completion_message)
    return completion_message

async def main():
    start_time = time.time()
    print("Starting all tasks concurrently...")
    tasks = [
        task("Task1", 2),
        task("Task2", 3),
        task("Task3", 1)
    ]
    results = await asyncio.gather(*tasks)
    print("\n--- All tasks have finished ---")
    print("Results collected:", results)
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())