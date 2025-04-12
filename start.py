import asyncio
from bot import main as run_bot
from scheduler import run_scheduler


async def start_all():
    await asyncio.gather(
        run_bot(),
        run_scheduler()
    )

if __name__ == "__main__":
    asyncio.run(start_all())
