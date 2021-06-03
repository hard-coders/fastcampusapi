from fastapi import FastAPI

from app import models

app = FastAPI()


@app.on_event("startup")
def on_startup():
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def hello():
    return b"hello World!"
