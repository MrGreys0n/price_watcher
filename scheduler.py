import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.scheduler import notify_price_changes


async def run_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_price_changes, IntervalTrigger(minutes=2))
    scheduler.start()
    print("✅ Планировщик запущен (каждые 2 мин, только для тестирования)")
    while True:
        await asyncio.sleep(3600)  # чтобы не выходил из цикла

if __name__ == "__main__":
    asyncio.run(run_scheduler())
