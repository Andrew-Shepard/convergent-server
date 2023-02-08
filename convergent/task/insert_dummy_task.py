# Please refactor this code into a relevant file :^) and delete it

import asyncio
from aiopg.sa import Engine
import psycopg2
from dependencies.logger import logger


class ඞ:
    def __init__(self, db: Engine) -> None:
        self.db = db

    async def start_task(self):
        while True:
            try:
                await self.task()
            except asyncio.CancelledError:
                raise
            except psycopg2.InterfaceError as e:
                logger.info(f"Had interface error, reconnecting. Exception was: {e}")
                await self.db.disconnect()
                await self.db.connect()
                continue
            await asyncio.sleep(120)

    async def task(self):
        pass
