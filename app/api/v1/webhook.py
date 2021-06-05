from fastapi import APIRouter, Body, Request, Depends
from pydantic import HttpUrl
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from app import models, schemas
from app.config import settings
from app.database import get_db
from app.lib import telegram

router = APIRouter()
bot = telegram.Telegram(settings.TELEGRAM_BOT_TOKEN)


def add_user(user: schemas.User, db: Session) -> models.User:
    row = models.User(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(row)
    db.commit()
    return row


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
    message = update.message
    user = update.message.from_

    db_user = db.query(models.User).filter_by(id=user.id).first()
    if not db_user:
        add_user(user, db)

    msg = "✨ '문제' 또는 '퀴즈'라고 말씀하시면 문제를 냅니다!"
    if "문제" in message.text or "퀴즈" in message.text:
        quiz = db.query(models.Quiz).order_by(func.RAND()).first()
        db_user.quiz_id = quiz.id
        msg = f"{quiz.question}\n\n{quiz.content}"
    elif db_user.quiz_id and message.text.isnumeric():
        correct = db_user.quiz.answer == int(message.text)
        msg = f"아쉽네요, {db_user.quiz.answer}번이 정답입니다."

        if correct:
            db_user.score += 1
            msg = f"{db_user.quiz.answer}번, 정답입니다!"

        db_user.quiz_id = None

    await bot.send_message(message.chat.id, msg)
    db.commit()

    return "OK"
