from fastapi import APIRouter
from . import v1, deps

router = APIRouter()
router.include_router(v1.router, prefix="/v1")
