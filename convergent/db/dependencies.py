from aiopg.sa import create_engine, Engine
from fastapi import Depends
from convergent.db.repos.user import UserRepo
from convergent.db.repos.answer import AnswerRepo
from convergent.db.repos.bible import BibleRepository

_db = None
CONN_SCHEMA = "postgresql"


async def init_db(host, port, user, password, database):
    global _db
    if _db is not None:
        raise RuntimeError("database is already initialized")
    db_uri = f"{CONN_SCHEMA}://{user}:{password}@{host}:{port}/{database}"
    _db = await create_engine(db_uri)


async def disconnect_db():
    global _db
    if _db is None:
        raise RuntimeError("database is not initialized")
    _db.terminate()
    await _db.wait_closed()
    _db = None


def get_db() -> Engine:
    if _db is None:
        raise RuntimeError("database is not initialized")
    return _db


def get_user_repository(db_engine=Depends(get_db)) -> UserRepo:
    return UserRepo(db=db_engine)


def get_answer_repository(db_engine=Depends(get_db)) -> AnswerRepo:
    return AnswerRepo(db=db_engine)


def get_bible_repository(db_engine=Depends(get_db)) -> BibleRepository:
    return BibleRepository(db=db_engine)
