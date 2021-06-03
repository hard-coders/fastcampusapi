from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST"},
    allow_headers={"*"},
)


@app.on_event("startup")
def on_startup():
    from app import models
    from app.database import engine

    models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def healthcheck():
    return {"ok": True}


app.include_router(api.router)
