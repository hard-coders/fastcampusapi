from fastapi import APIRouter, Depends

from app.api.deps import verify_telegram_login


router = APIRouter()


@router.post("")
async def verfiy_telegram(token: str = Depends(verify_telegram_login)):
    return {"token": token}
