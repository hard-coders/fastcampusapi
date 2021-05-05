from typing import Any, Optional, Dict

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse


class SomeError(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

    def __str__(self):
        return f"<{self.name}> is occured. code: <{self.code}>"


class SomeFastAPIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, headers=headers
        )


app = FastAPI()


@app.exception_handler(SomeError)
async def some_error_handler(request: Request, exc: SomeError):
    return JSONResponse(
        content={"message": f"error is {exc.name}"}, status_code=exc.code
    )


users = {
    1: {"name": "Fast"},
    2: {"name": "Campus"},
    3: {"name": "API"},
}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"<User: {user_id}> is not exists.",
        )
    return users[user_id]


@app.get("/error")
async def get_error():
    raise SomeError("Hello", 500)
