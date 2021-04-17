import uvicorn

from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl


app = FastAPI()


class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser):
    return user


if __name__ == "__main__":
    uvicorn.run(app)
