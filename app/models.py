from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    score = Column(Integer, default=0)
