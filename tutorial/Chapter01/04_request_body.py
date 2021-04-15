from typing import Optional

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    password: str
    avatar_url: Optional[HttpUrl] = None


@app.post("/users")
def create_user(user: User):
    return user


if __name__ == "__main__":
    uvicorn.run(app)
