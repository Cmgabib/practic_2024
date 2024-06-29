from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.answers import Answers
from db.queue_platform import Queue_platform


class Request:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def select_answers(self, condition: str) -> dict:
        sql = await self.session.execute(
            select(Answers.message, Answers.photo_id, Answers.file_id).where(
                Answers.command == condition
            )
        )
        data = sql.fetchone()
        if data is not None:
            keys = ("message", "photo_id", "file_id")
            my_dict = dict(zip(keys, data))
            return my_dict
        else:
            return None