from typing import List, Optional, Union
from enum import Enum
from fastapi import APIRouter, Depends, Response, status

from convergent.db.schemas.user import User
from convergent.db.schemas.answer import Answer

from convergent.db.repos.user import UserRepo
from convergent.db.repos.answer import AnswerRepo
from convergent.db.repos.bible import BibleRepository
from convergent.db.models.books import bible_chapters, bible_chapters_list

from convergent.db.dependencies import (
    get_answer_repository,
    get_bible_repository,
    get_user_repository,
)
from convergent.dependencies.auth_handler import signJWT
from convergent.dependencies.auth_bearer import JWTBearer

from convergent.dependencies.logger import logger

import random
import datetime

public_router = APIRouter()
public_tags: Optional[List[Union[str, Enum]]] = ["public"]


@public_router.post(
    "/login", tags=public_tags,
)
async def login(
    login_user: User,
    response: Response,
    user_repo: UserRepo = Depends(get_user_repository),
):
    validate = await user_repo.login(login_user=login_user)

    if validate == True:
        return signJWT(user_id=login_user.user_id)
    else:
        return {"error": "Wrong login details!"}


@public_router.post(
    "/register", tags=public_tags,
)
async def register(new_user: User, user_repo: UserRepo = Depends(get_user_repository)):
    try:
        await user_repo.create_user(new_user=new_user)
    except Exception as e:
        logger.error(f"Error from endpoint /register: {e}")
        if 'duplicate key' in str(e):
            return {"error": "Username is already taken."}
        return {"error": "Could not create user."}

    return {"message": f"{new_user.user_id} registered!"}


@public_router.patch(
    "/add_partner", tags=public_tags, dependencies=[Depends(JWTBearer())]
)
async def add_partner(user: User, user_repo: UserRepo = Depends(get_user_repository)):
    await user_repo.add_partner(user=user)


@public_router.post(
    "/get_partner", tags=public_tags, dependencies=[Depends(JWTBearer())]
)
async def get_partner(user: User, user_repo: UserRepo = Depends(get_user_repository)):
    partner = await user_repo.get_partner(user=user)
    return {"partner": partner}


@public_router.get("/chapter", tags=public_tags, dependencies=[Depends(JWTBearer())])
async def get_chapter(bible_repo: BibleRepository = Depends(get_bible_repository)):
    # Get the current date
    today = datetime.date.today()

    # Use the day of the year as the daily seed for the random number generator
    daily_seed = today.timetuple().tm_yday

    # Select a random book
    random.seed(daily_seed)
    book = random.choice(list(bible_chapters.keys()))

    # Get the number of chapters in the selected book
    chapter_count = bible_chapters[book]

    # Use the daily seed to select a random chapter index for the selected book
    random.seed(daily_seed)
    chapter = random.randint(1, chapter_count)

    book_index = bible_chapters_list.index(book)

    chapter_text = await bible_repo.get_chapter(book=book_index, chapter=chapter)
    # Return the selected chapter
    return {"book": book, "chapter": chapter, "chapter_text": chapter_text}


@public_router.post("/answer", tags=public_tags, dependencies=[Depends(JWTBearer())])
async def mark_answered(
    user: User, answer_repo: AnswerRepo = Depends(get_answer_repository)
):
    # Pass user's code
    # Mark user as having answered
    # TODO: Verify User vs User Token
    await answer_repo.mark_answered(user=user)
    return {"answered": True}


@public_router.post(
    "/has_answered", tags=public_tags, dependencies=[Depends(JWTBearer())]
)
async def get_has_answered(
    partner: User, answer_repo: AnswerRepo = Depends(get_answer_repository)
):
    # Pass partner code
    answer = await answer_repo.get_answered(partner)
    if answer == None:
        return {"answered": False}

    if answer.answered == True:
        # Return if code has been marked as answered for today
        return {"answered": True}

    return {"answered": False}
