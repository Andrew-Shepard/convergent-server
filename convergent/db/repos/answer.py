from typing import List
from convergent.db.schemas.answer import Answer
from convergent.db.schemas.user import User
from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import ANSWER


class AnswerRepo(BaseRepository):
    async def mark_answered(self, user: User):
        sql_query = ANSWER.insert(user.user_id, True)

        async with self.db.acquire() as conn:
            conn.execute(sql_query)

    async def clear_answered(self):
        sql_query = (
            ANSWER.update().where(ANSWER.c.answered == True).values(answered=False)
        )

        async with self.db.acquire() as conn:
            conn.execute(sql_query)

    async def get_answered(self, user: User) -> Answer:
        sql_query = ANSWER.select().where(ANSWER.c.user_id == user.user_id)

        async with self.db.acquire() as conn:
            return conn.execute(sql_query)
