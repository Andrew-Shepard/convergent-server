from typing import List
import bcrypt
from convergent.db.schemas.user import User
from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import USER

class UserRepo(BaseRepository):
    async def create_user(self, new_user: User):
        password = new_user.password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password=password, salt=salt).decode("utf-8")
        new_user.password = hash

        sql_query = USER.insert().values(
            user_id=new_user.user_id,
            password=new_user.password,
            partner_id=new_user.partner_id,
        )
        async with self.db.acquire() as conn:
            await conn.execute(sql_query)

    async def login(self, login_user: User):
        sql_query = USER.select().where((USER.c.user_id == login_user.user_id))
        async with self.db.acquire() as conn:
            async for row in conn.execute(sql_query):
                matched_db_user = User.parse_obj(row)
                if bcrypt.checkpw(
                    password=login_user.password.encode("utf-8"),
                    hashed_password=matched_db_user.password.encode("utf-8"),
                ):
                    return True
        return False

    async def add_partner(self, user: User):
        sql_query = (
            USER.update()
            .where(USER.c.user_id == user.user_id)
            .values(partner_id=user.partner_id)
        )
        async with self.db.acquire() as conn:
            await conn.execute(sql_query)

    async def get_partner(self, user: User) -> str:
        sql_query = USER.select().where(USER.c.user_id == user.user_id)
        async with self.db.acquire() as conn:
            async for row in conn.execute(sql_query):
                matched_db_user = User.parse_obj(row)
                return matched_db_user.partner_id

