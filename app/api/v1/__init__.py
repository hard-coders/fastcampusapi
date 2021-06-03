from fastapi import APIRouter

from . import webhook, user


router = APIRouter()
router.include_router(webhook.router, prefix="/webhook")
router.include_router(user.router, prefix="/users", tags=["User"])
