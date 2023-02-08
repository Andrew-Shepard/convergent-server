from typing import List
from convergent.db.schemas.question import Question
from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import QUESTION


class QuestionRepo(BaseRepository):
    async def get_question():
        # To be implemented after question repo
        pass
