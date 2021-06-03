from fastapi import APIRouter, Body, Request
from pydantic import HttpUrl

from app.config import settings
from app.lib import telegram
from devtools import debug

router = APIRouter()
bot = telegram.Telegram(settings.TELEGRAM_BOT_TOKEN)


@router.get("")
async def get_webhook():
    return await bot.get_webhook()


@router.post("")
async def set_webhook(url: HttpUrl = Body(..., embed=True)):
    return await bot.set_webhook(url)


@router.post(f"/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}")
async def webhook(request: Request):
    r = await request.json()
    r = telegram.schema.Update.parse_obj(r)
    debug(r)
    return "OK"
