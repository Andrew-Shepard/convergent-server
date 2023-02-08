from typing import List
import string
import random
from convergent.db.schemas.user import User
from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import USER


class UserRepo(BaseRepository):
    async def create_user(self):
        # Generate (A-Z + 0-9) 6 digits
        def generate_id() -> str:
            return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        async def check_unique(user_id: str) -> bool:
            # Verify doesn't already exist
            sql_query = USER.select().where(USER.c.user_id == user_id)
            async with self.db.acquire() as conn:
                if await conn.execute(sql_query):
                    return False
            return True

        new_id = generate_id()
        # If it does regenerate
        while await check_unique(new_id) == False:
            new_id = generate_id()

        # Add as a generated code
        sql_query = USER.insert().values(user_id=new_id)

        async with self.db.acquire() as conn:
            await conn.execute(sql_query)

        # Return generated code
        return new_id
