import hmac
from hashlib import sha256
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session

from app import models
from app.config import settings
from app.database import get_db


security = HTTPBearer()


class AuthTelegram(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    photo_url: str
    auth_date: str
    hash: str


async def create_access_token(auth: AuthTelegram, exp: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (exp or timedelta(minutes=30))
    data = {
        "id": int(auth.id),
        "username": auth.username,
        "photo_url": auth.photo_url,
        "exp": expire,
    }

    return jwt.encode(data, settings.SECRET_KEY.get_secret_value(), algorithm="HS256")


async def verify_telegram_login(auth: AuthTelegram) -> str:
    """
    See: https://core.telegram.org/widgets/login#checking-authorization
    """
    data = auth.dict()
    hash_ = data.pop("hash")
    bot_token = settings.TELEGRAM_BOT_TOKEN.get_secret_value()

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = sha256(bot_token.encode()).digest()

    h = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=sha256)

    if hmac.compare_digest(h.hexdigest(), hash_):
        return await create_access_token(auth)
    raise HTTPException(401, "Failed to verify Telegram")


async def get_user(
    cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> models.User:
    token = cred.credentials
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), "HS256")
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")

    db_user = db.query(models.User).filter(models.User.id == decoded_data.get("id")).first()
    if not db_user:
        raise HTTPException(401, "Not registred")

    return db_user
