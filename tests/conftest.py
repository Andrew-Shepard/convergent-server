import pytest
import pytest_asyncio
import datetime
import respx
import bcrypt
from os import getenv
from aiopg.sa import create_engine
from httpx import AsyncClient

from convergent.api import create_app
from convergent.settings import get_settings, Settings
from convergent.db.dependencies import get_db
from convergent.db.models.models import USER, ANSWER, BIBLE


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
        await conn.execute("TRUNCATE answer, users, bible CASCADE")
    db.terminate()
    await db.wait_closed()


@pytest_asyncio.fixture
async def populate_db(db):
    username = getenv("USERNAME")
    password = getenv("PASSWORD")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    insert = [
        "INSERT INTO \"bible\" VALUES(0,1,1,'In the beginning God created the heaven and the earth.');",
        "INSERT INTO \"bible\" VALUES(0,1,2,'And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.');",
        "INSERT INTO \"bible\" VALUES(0,1,3,'And God said, Let there be light: and there was light.');",
        "INSERT INTO \"bible\" VALUES(0,1,4,'And God saw the light, that it was good: and God divided the light from the darkness.');",
        USER.insert().values(
            user_id="{}".format(username),
            password=hashed_password.decode("utf-8"),
            partner_id="test_partner",
        ),
        USER.insert().values(
            user_id="test_partner", password=hashed_password.decode("utf-8"),
        ),
    ]

    async with db.acquire() as conn:
        for item in insert:
            await conn.execute(item)
