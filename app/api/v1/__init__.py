from fastapi import APIRouter

from . import webhook


router = APIRouter()
router.include_router(webhook.router, prefix="/webhook")
