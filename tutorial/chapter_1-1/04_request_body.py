from typing import Optional, List

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    amount: int = 0


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None
    inventory: List[Item] = []


@app.post("/users")
def create_user(user: User):
    return user


@app.get("/users/me")
def get_user():
    fake_user = User(
        name="FastCampus",
        password="1234",
        inventory=[
            Item(name="전설 무기", price=1_000_000),
            Item(name="전설 방어구", price=900_000),
        ]
    )
    return fake_user


if __name__ == "__main__":
    uvicorn.run(app)
