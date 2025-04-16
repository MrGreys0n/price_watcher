from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .scheduler import notify_price_changes
import atexit

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(notify_price_changes, IntervalTrigger(minutes=60))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
