from typing import List, Optional, Union
from enum import Enum
from fastapi import APIRouter, Depends

from convergent.db.schemas.user import User
from convergent.db.schemas.answer import Answer
from convergent.db.schemas.question import Question

from convergent.task.generate_questions import generate

from convergent.dependencies.logger import logger

import random

public_router = APIRouter()
public_tags: Optional[List[Union[str, Enum]]] = ["public"]


@public_router.get(
    "/question", tags=public_tags,
)
async def get_question() -> Question:
    # Based on server's date, can think of a better way later
    # Return generated question, should be from db in future
    return generate()[random.randint(0, 1)]


@public_router.post(
    "/answer", tags=public_tags,
)
async def mark_answered():
    # Pass user's code
    # Mark user as having answered
    pass


@public_router.get(
    "/has_answered", tags=public_tags,
)
async def get_has_answered():
    # Pass partner code
    # Return if code has been marked as answered for today
    pass
