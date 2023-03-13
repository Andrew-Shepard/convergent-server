from typing import List
from convergent.db.schemas.answer import Answer
from convergent.db.schemas.user import User
from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import ANSWER
from datetime import date
import uuid


class AnswerRepo(BaseRepository):
    async def mark_answered(self, user: User):
        today = date.today()
        answer_id = str(uuid.uuid4())
        sql_query = ANSWER.insert().values(
            answer_id=answer_id, date=today, user_id=user.user_id, answered=True,
        )

        async with self.db.acquire() as conn:
            await conn.execute(sql_query)

    async def get_answered(self, user: User) -> Answer:
        today = date.today()
        sql_query = ANSWER.select().where(
            ANSWER.c.user_id == user.user_id, ANSWER.c.date == today
        )
        async with self.db.acquire() as conn:
            async for row in conn.execute(sql_query):
                return Answer.parse_obj(row)
