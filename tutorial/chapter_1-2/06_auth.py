from fastapi import Depends, FastAPI
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)


app = FastAPI()
security = HTTPBasic()
security_bearer = HTTPBearer()


@app.get("/basic")
async def get_current_user_basic(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}


@app.get("/bearer")
async def get_current_user_bearer(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
):
    return credentials
