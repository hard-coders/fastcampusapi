import uvicorn

from fastapi import FastAPI, Header, Cookie

app = FastAPI()


@app.get("/cookie")
def get_cookies(ga: str = Cookie(None, title="구글 애널리틱스", example="GA1.2.3")):
    return {"ga": ga}


@app.get("/header")
def get_headers(x_token: str = Header(None, title="토큰")):
    return {"X-Token": x_token}


if __name__ == "__main__":
    uvicorn.run(app)
