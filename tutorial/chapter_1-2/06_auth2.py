from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import ExpiredSignatureError


app = FastAPI()
security = HTTPBearer()

ALGORITHM = "HS256"
# openssl rand -hex 32
# python -c "import secrets;print(secrets.token_hex(32))"
SECRET_KEY = "e9f17f1273a60019da967cd0648bdf6fd06f216ce03864ade0b51b29fa273d75"
fake_user_db = {
    "fastcampus": {
        "id": 1,
        "username": "fastcampus",
        "email": "fastcampus@fastcampus.com",
        # bcrypt.hashpw("password".encode(), bcrypt.gensalt())
        "password": "$2b$12$kEsp4W6Vrm57c24ez4H1R.rdzYrXipAuSUZR.hxbqtYpjPLWbYtwS",
    }
}


class User(BaseModel):
    id: int
    username: str
    email: str


class UserPayload(User):
    exp: datetime


async def create_access_token(data: dict, exp: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (exp or timedelta(minutes=30))
    user_info = UserPayload(**data, exp=expire)

    return jwt.encode(user_info.dict(), SECRET_KEY, algorithm=ALGORITHM)


async def get_user(cred: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = cred.credentials
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(401, "Expired")
    user_info = User(**decoded_data)

    return fake_user_db[user_info.username]


@app.post("/login")
async def issue_token(data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db[data.username]

    if bcrypt.checkpw(data.password.encode(), user["password"].encode()):
        return await create_access_token(user, exp=timedelta(minutes=30))
    raise HTTPException(401)


@app.get("/users/me", response_model=User)
async def get_current_user(user: dict = Depends(get_user)):
    return user
