import pytest
import pytest_asyncio
import datetime
import respx
from os import getenv
from aiopg.sa import create_engine
from httpx import AsyncClient

from convergent.api import create_app
from convergent.settings import get_settings, Settings
from convergent.db.dependencies import get_db
from convergent.db.models.models import USER, ANSWER, QUESTION


@pytest.fixture
def app(settings, db):
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    app.dependency_overrides[get_db] = lambda: db
    return app


@pytest.fixture
def client(app):
    respx.route(host="test").pass_through()
    aclient = AsyncClient(app=app, base_url="http://test")
    return aclient


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def db_url():
    host = getenv("POSTGRES_HOST", "test_db")
    port = getenv("POSTGRES_PORT", "5432")
    username = getenv("POSTGRES_USER", "postgres")
    password = getenv("POSTGRES_PASSWORD", "postgres")
    database = getenv("POSTGRES_DB", "postgres")
    return "postgresql://{username}:{password}@{host}:{port}/{database}".format(
        username=username, password=password, host=host, port=port, database=database,
    )


@pytest_asyncio.fixture
async def db(db_url):
    db = await create_engine(db_url)
    yield db
    async with db.acquire() as conn:
        await conn.execute("TRUNCATE answer, user, question CASCADE")
    db.terminate()
    await db.wait_closed()


@pytest_asyncio.fixture
async def populate_db(db):
    insert = [ANSWER.insert(), USER.insert(), QUESTION.insert()]

    async with db.acquire() as conn:
        for item in insert:
            await conn.execute(item)
