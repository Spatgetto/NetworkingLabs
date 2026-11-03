import asyncio

async def main():
    print("Starting asyncio test...")
    await asyncio.sleep(1)
    print("Asyncio test completed.")

if __name__ == "__main__":
    asyncio.run(main())
    