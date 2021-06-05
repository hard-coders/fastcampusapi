from sqlalchemy import Column, Integer, String, DateTime, func, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from app.database import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp()
    )


class User(BaseMixin, Base):
    __tablename__ = "user"

    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=True)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    score = Column(Integer, default=0)

    quiz = relationship("Quiz", back_populates="current_users", uselist=False)


class Quiz(BaseMixin, Base):
    __tablename__ = "quiz"

    question = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    answer = Column(Integer, nullable=False)

    current_users = relationship("User", back_populates="quiz")
