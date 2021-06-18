from typing import List

from fastapi import APIRouter, Depends, status, Form
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from app import models, schemas
from app.database import get_db


router = APIRouter()


async def add_quiz(question: str, content: str, answer: int, db: Session) -> models.Quiz:
    row = models.Quiz(question=question, content=content, answer=answer)
    db.add(row)
    db.commit()

    return row


@router.get("", response_model=List[schemas.Quiz])
async def get_quiz_list(db: Session = Depends(get_db)):
    return db.query(models.Quiz).all()


@router.post("", response_model=schemas.ResourceId, status_code=status.HTTP_201_CREATED)
async def create_quiz(data: schemas.QuizCreate, db: Session = Depends(get_db)):
    return await add_quiz(**data.dict(), db=db)


@router.post("/form", response_model=schemas.ResourceId, status_code=status.HTTP_201_CREATED)
async def create_quiz_redirect(
    question: str = Form(..., title="퀴즈 질문"),
    content: str = Form(..., title="퀴즈 내용"),
    answer: int = Form(..., title="정답"),
    db: Session = Depends(get_db),
):
    return await add_quiz(question, content, answer, db)


@router.get("/random", response_model=schemas.Quiz)
async def get_quiz_randomly(db: Session = Depends(get_db)):
    return db.query(models.Quiz).order_by(func.RAND()).first()
