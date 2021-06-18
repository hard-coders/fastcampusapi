from fastapi import APIRouter, Depends

from app.api.deps import get_user
from . import webhook, user, quiz, auth


router = APIRouter()
router.include_router(webhook.router, prefix="/webhook", dependencies=[Depends(get_user)])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(user.router, prefix="/users", tags=["User"], dependencies=[Depends(get_user)])
router.include_router(
    quiz.router, prefix="/quizzes", tags=["Quiz"], dependencies=[Depends(get_user)]
)
