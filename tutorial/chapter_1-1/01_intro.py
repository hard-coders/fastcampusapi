import uvicorn

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    uvicorn.run(app)
