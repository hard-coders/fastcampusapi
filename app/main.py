from fastapi import FastAPI, Body, Request
from pydantic import HttpUrl

from app import models
from app.config import settings
from app.lib import telegram
from devtools import debug


app = FastAPI()
bot = telegram.Telegram(settings.TELEGRAM_BOT_TOKEN)


@app.on_event("startup")
def on_startup():
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def hello():
    return b"hello World!"


@app.post("/")
async def webhook(request: Request):
    r = await request.json()
    r = telegram.schema.Update.parse_obj(r)
    debug(r)
    return 'OK'


@app.get("/me")
async def get_me():
    return await bot.get_bot_info()


@app.get("/wb")
async def get_webhook():
    return await bot.get_webhook()


@app.post("/wb")
async def set_webhook(url: HttpUrl = Body(..., embed=True)):
    return await bot.set_webhook(url)
