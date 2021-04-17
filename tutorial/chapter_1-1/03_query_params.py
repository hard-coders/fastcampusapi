from enum import Enum

import uvicorn

from fastapi import FastAPI

app = FastAPI()


class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"


@app.get("/users")
def get_users(is_admin: bool, limit: int = 100):
    return {"is_admin": is_admin, "limit": limit}


@app.get("/users/grade")
def get_users_grade(grade: UserLevel = UserLevel.a):
    return {"grade": grade}


if __name__ == "__main__":
    uvicorn.run(app)
