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
async def startup_event():
    from app.database import engine, Base

    Base.metadata.create_all(bind=engine)


@app.get("/")
async def healthcheck():
    return {"ok": True}


app.include_router(api.router)
