import pytest
from httpx import AsyncClient

from app import main, models
from app.database import engine, get_db
from app.config import settings


@pytest.fixture(scope="session")
def app():
    if not settings.TESTING:
        raise SystemError("TESTING environment must be set true")

    return main.app


@pytest.fixture
async def session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
async def default_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test/v1") as ac:
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)
        yield ac


@pytest.fixture
def user(session) -> models.User:
    row = models.User(username="fc2021", first_name="fast", last_name="campus")
    session.add(row)
    session.commit()

    return row


@pytest.fixture
def add_quiz(session):
    def func(question: str = None, content: str = None, answer: int = None) -> models.Quiz:
        r = models.Quiz(
            question=question or "qqq",
            content=content or "text",
            answer=answer or 1,
        )
        session.add(r)
        session.commit()
        return r

    return func
