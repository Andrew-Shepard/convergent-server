from convergent.db.repos.base import BaseRepository
from convergent.db.models.models import BIBLE
import gzip


class BibleRepository(BaseRepository):
    async def get_chapter(self, book: int, chapter: int):
        sql_query = f"""SELECT *
                FROM bible
                WHERE {BIBLE.c.book} = {book} AND {BIBLE.c.chapter} = {chapter}
                ORDER BY bible.Versecount ASC;
                """

        # Execute the select statement and retrieve the result
        async with self.db.acquire() as conn:
            result = await conn.execute(sql_query)
            chapter_rows = await result.fetchall()

        # Concatenate the text of all verses in the chapter
        chapter_text = "\n".join([row[BIBLE.c.verse] for row in chapter_rows])

        # Compress the response using gzip compression
        return chapter_text
