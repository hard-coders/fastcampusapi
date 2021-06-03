from fastapi import APIRouter, Body, Request, Depends
from pydantic import HttpUrl
from sqlalchemy.orm.session import Session

from app import models
from app.config import settings
from app.database import get_db
from app.lib import telegram

router = APIRouter()
bot = telegram.Telegram(settings.TELEGRAM_BOT_TOKEN)


@router.get("")
async def get_webhook():
    return await bot.get_webhook()


@router.post("")
async def set_webhook(url: HttpUrl = Body(..., embed=True)):
    return await bot.set_webhook(url)


@router.post(f"/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}")
async def webhook(request: Request, db: Session = Depends(get_db)):
    resp = await request.json()
    update = telegram.schema.Update.parse_obj(resp)
    user = update.message.from_
    db_user = db.query(models.User).filter_by(id=user.id).first()

    if not db_user:
        row = models.User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        db.add(row)
        db.commit()
    return "OK"
