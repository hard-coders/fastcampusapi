from fastapi import FastAPI

from app import models
from app.config import settings
from lib.telegram import Telegram


app = FastAPI()
telegram = Telegram(settings.TELEGRAM_BOT_TOKEN)


@app.on_event("startup")
def on_startup():
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def hello():
    return b"hello World!"


@app.get("/me")
async def get_me():
    return await telegram.get_bot_info()
