import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app.routers import favorites, profile, search


app = FastAPI()

# Static / Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(favorites.router)
app.include_router(profile.router)
app.include_router(search.router)
